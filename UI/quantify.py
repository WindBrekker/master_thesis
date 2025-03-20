import sys
import shutil
import os
import numpy as np
from pathlib import Path
from os.path import exists as file_exists
from PyQt6.QtGui import QPalette, QColor, QIcon, QAction, QPixmap
from PyQt6.QtWidgets import QApplication, QMessageBox
import new_window
import mode1
import mode2
import mode3
import start_window
import matplotlib.pyplot as plt
from tqdm import tqdm
import xraylib as xr
import math
import utils


def quantify(window, main_folder_path, pixel_size_value, inputfile_name, 
             zeropeak_name, scatter_name, sample_matrix_name, treshhold_value, 
             spectrum, zeropeak_coefficients_name, scatter_coefficients_name):
    print("Quantifying...")
    folder = window.current_folder_name
    # Create folder for outputs
    if not Path.joinpath(main_folder_path, "temporary").exists():
        Path.joinpath(main_folder_path, "temporary").mkdir()
    if not Path.joinpath(main_folder_path, "temporary", f"{folder}_output").exists():
        Path.joinpath(main_folder_path, "temporary", f"{folder}_output").mkdir()
    window.temporary_folder = Path.joinpath(main_folder_path, "temporary", f"{folder}_output")
    print("temporary folder created.")
    
    scater_tab = np.array(utils.file_to_list(Path.joinpath(window.subfolder_path, f"{window.prename}{scatter_name}")))
    if spectrum == "Poli":
        scater_tab = scater_tab/window.livetime_matrix
    print("Scater table calculated.")
        
    # Create arrays for calculations
    surface_mass_array = []
    sample_mass_livetime = np.zeros_like(scater_tab)
    antimask_scater = np.zeros_like(scater_tab)
    antimask_scater_mask = np.zeros_like(scater_tab)
    antimask_scater_masked = np.zeros_like(scater_tab)

    antimask_scater = scater_tab * window.antimask

    scater_treshold = np.min(scater_tab)
    
    antimask_scater_mask = (window.antimask & (antimask_scater < (1.25 * scater_treshold))).astype(int)

    utils.output_to_file(antimask_scater_mask, Path.joinpath(window.temporary_folder, "antimask_scater_mask"))
    
    print("Antimask scater mask calculated.")
    
    antimask_scater_masked = antimask_scater * antimask_scater_mask
    iteration_antimask = np.count_nonzero(antimask_scater_mask)
    print(f"Antimask scater masked calculated. Iteration: {iteration_antimask}")
    
    antimask_mean = np.mean(antimask_scater_masked[antimask_scater_masked != 0]) if iteration_antimask != 0 else 0
    
    plt.imshow(antimask_scater_mask, cmap=window.color_of_heatmap, interpolation="nearest")
    plt.savefig("antimask_plot.png")

    difference = scater_tab - float(antimask_mean)


    sample_mass_livetime = np.where(difference > 0, difference, 0)
    surface_mass_array = np.array(utils.SampSM_calc(sample_mass_livetime, float(window.scater_dict["a"]), float(window.scater_dict["b"])))
    surface_mass_array_masked = np.multiply(surface_mass_array, window.mask)
    
    utils.output_to_file(surface_mass_array_masked, Path.joinpath(window.temporary_folder, "sample_mass_noc"))
    print("Sample mass calculated.")
    for key in window.elements_in_subfolder:
            element_line = key
            element = element_line.split()[0]
            try:
                line = element_line.split()[1]
            except Exception as e:
                line = "K"
                print (f"Error: {e}")
            
            print(f"Processing element: {element} ...")
            if Path.joinpath(window.subfolder_path, f"{window.prename}{element_line}.txt").exists() or Path.joinpath(window.subfolder_path, f"{window.prename}{element_line}.csv").exists():
                K_i = float(window.k_value_per_element_dict[element])
                counts_data = Path.joinpath(window.subfolder_path,f"{window.prename}{element}")
                counts_table = utils.file_to_list(counts_data)
                table_of_smi = np.zeros_like(counts_table)
                print("Counts table loaded.")
                
                counts_table = np.array(counts_table, dtype=float)
                mask_map = np.array(window.mask, dtype=float)
                if spectrum == "Poli":
                    window.livetime_matrix = np.array(window.livetime_matrix, dtype=float)
                    table_of_smi = (counts_table * mask_map) / window.livetime_matrix / K_i
                elif spectrum == "Mono":
                    table_of_smi = (counts_table * mask_map) / K_i
                utils.output_to_file(table_of_smi,Path.joinpath(window.temporary_folder,f"{element_line}_table_of_smi"))    
                print("SMi table calculated.")             
                        
                
                Ci_table = np.zeros_like(table_of_smi)
                Ci_table_no_heatpoints = np.zeros_like(table_of_smi)
                lambda_factor = np.zeros_like(table_of_smi)
                median_value = np.median(surface_mass_array)
                total_elements = surface_mass_array.size
                print("total elements", total_elements)
                indices = np.argwhere(table_of_smi != 0)
                
                counter = 0
                number = 0
                Ci_table_sum = 0
                lambda_factor_sum = 0
                
                print("Calculating lambda factor and Ci...")
                
                for i, j in tqdm(indices, desc="Processing elements"):
                    value = surface_mass_array[i, j]
                    smi_value = table_of_smi[i, j]
                    lambda_factor_value = utils.calculate_lambda_factor(value, int(window.z_number_per_element_dict[element]),float(window.energy_per_element_dict[element]), window.concentration_per_element_dict )
                    lambda_factor[i, j] = lambda_factor_value
                    
                    if value > 0.3 * median_value and smi_value >= 0:
                        Ci_table[i, j] = (smi_value * lambda_factor_value / value)
                        number += 1                        
                    else:
                        Ci_table[i, j] = 0
                    counter +=1
                    Ci_table_sum += Ci_table[i, j]
                    lambda_factor_sum += lambda_factor_value
                utils.output_to_file(Ci_table, Path.joinpath(window.temporary_folder, f"{element_line}_Ci_table"))
                utils.output_to_file(lambda_factor, Path.joinpath(window.temporary_folder, f"{element_line}_lambda_factor"))
            
                    
                Ci_table_sum_2 = np.sum(Ci_table[table_of_smi != 0])        
                lambda_average_factor = lambda_factor_sum/counter
                Ci_average_factor = Ci_table_sum/counter
                Ci_average_factor_2 = Ci_table_sum_2/counter
                print(f"Avg Ci1: {Ci_average_factor:.2e}. Avg Ci2: {Ci_average_factor_2:.2e}")
                
                
                for i, j in tqdm(np.ndindex(Ci_table.shape), desc="Processing Ci_table elements"):
                    if Ci_table[i, j] > 10*float(Ci_average_factor):
                        Ci_table_no_heatpoints[i, j] = 0   
                    else:
                        Ci_table_no_heatpoints[i, j] = Ci_table[i, j]
                utils.output_to_file(Ci_table_no_heatpoints, Path.joinpath(window.temporary_folder, f"{element_line}_Ci_table_no_heatpoints"))
    print("Quantification finished.")
    QMessageBox.information(window,"Qunatification Completed", "Use arrows to see Ci maps. \nUse 'confirm' button to save data. \nUse 'current subfolder combobox' to continue with next data.")
    window.previous_element_button.clicked.connect(lambda: utils.previous_ci_map(window))
    window.next_element_button.clicked.connect(lambda: utils.next_ci_map(window))
    window.confirm_saving_button.setEnabled(True)
    
