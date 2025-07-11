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
import logging

logging.basicConfig(filename='quantify.log', level=logging.DEBUG)

def quantify(window, main_folder_path, pixel_size_value, inputfile_name, 
             zeropeak_name, scatter_name, sample_matrix_name, treshhold_value, 
             spectrum, zeropeak_coefficients_name, scatter_coefficients_name):
    print("Quantifying...")
    window.pixel_size = pixel_size_value
    folder = window.current_folder_name
    # Create folder for outputs
    if not Path.joinpath(main_folder_path, "temporary").exists():
        Path.joinpath(main_folder_path, "temporary").mkdir()
    if not Path.joinpath(main_folder_path, "temporary", f"{folder}_output").exists():
        Path.joinpath(main_folder_path, "temporary", f"{folder}_output").mkdir()
    window.temporary_folder = Path.joinpath(main_folder_path, "temporary", f"{folder}_output")
    window.output_path = Path.joinpath(main_folder_path, f"{folder}_output")
    
    #print("temporary folder created.")
    
    scater_tab = np.array(utils.file_to_list(Path.joinpath(window.subfolder_path, f"{window.prename}{scatter_name}")))
    if spectrum == "Poli":
        scater_tab = scater_tab/window.livetime_matrix
    print("Scater table calculated.")
    print(scater_tab.mean())
        
    # Create arrays for calculations
    surface_mass_array = []
    sample_mass_livetime = np.zeros_like(scater_tab)
    antimask_scater = np.zeros_like(scater_tab)
    antimask_scater_mask = np.zeros_like(scater_tab)
    antimask_scater_masked = np.zeros_like(scater_tab)

    antimask_scater = scater_tab * window.antimask
    
    plt.imshow(scater_tab, cmap=window.color_of_heatmap, interpolation="nearest")
    plt.savefig("scater_plot.png")
    
    plt.imshow(antimask_scater, cmap=window.color_of_heatmap, interpolation="nearest")
    plt.savefig("antimask_scater.png")

    scater_treshold = np.min(scater_tab)
    print(f"Scater treshold: {scater_treshold}")
    
    antimask_scater_mask = (window.antimask & (antimask_scater < (1.25 * scater_treshold))).astype(int)

    utils.output_to_file(antimask_scater_mask, Path.joinpath(window.temporary_folder, "antimask_scater_mask"))
    
    print("Antimask scater mask calculated.")
    
    antimask_scater_masked = antimask_scater * antimask_scater_mask
    iteration_antimask = np.count_nonzero(antimask_scater_mask)
    print(f"Antimask scater masked calculated. Iteration: {iteration_antimask}")
    
    antimask_mean = np.median(antimask_scater_masked[antimask_scater_masked != 0]) if iteration_antimask != 0 else 0
    
    plt.imshow(antimask_scater_masked, cmap=window.color_of_heatmap, interpolation="nearest")
    plt.savefig("antimasked_plot.png")
    
    plt.imshow(antimask_scater_mask, cmap=window.color_of_heatmap, interpolation="nearest")
    plt.savefig("antimask_plot.png")

    difference = scater_tab - float(antimask_mean)

    sample_mass_livetime = np.where(difference > 0, difference, 0)
    print(sample_mass_livetime)
    plt.imshow(sample_mass_livetime, cmap=window.color_of_heatmap, interpolation="nearest")
    plt.savefig("sample_mass_livetime.png")
    surface_mass_array = np.array(utils.SampSM_calc(sample_mass_livetime, float(window.scater_dict["a"]), float(window.scater_dict["b"])))
    surface_mass_array_masked = np.multiply(surface_mass_array, window.mask)
    
    surface_mass_array_masked_mean = np.median(surface_mass_array_masked[surface_mass_array_masked != 0])
    surface_mass_array_masked[surface_mass_array_masked <= 0.1 * surface_mass_array_masked_mean] = 0
    surface_mass_array_masked[surface_mass_array_masked >= 2 * surface_mass_array_masked_mean] = surface_mass_array_masked_mean
    
    print(f"Surface mass array masked mean: {surface_mass_array_masked_mean}")
    
    utils.output_to_file(surface_mass_array_masked, Path.joinpath(window.temporary_folder, "sample_mass_noc"))
    print("Sample mass calculated.")
    for key in window.elements_in_subfolder:
            element_line = key
            logging.info(f"Processing element: {element_line} ...")
            element = element_line.split("-")[0]
            try:
                line = element_line.split("-")[1]
            except Exception as e:
                line = "K"
                print (f"Error: {e}. Used default line: {line}")
            
            print(f"Processing element: {element_line} ...")
            if Path.joinpath(window.subfolder_path, f"{window.prename}{element_line}.txt").exists() or Path.joinpath(window.subfolder_path, f"{window.prename}{element_line}.csv").exists():
                try:
                    K_i = float(window.k_value_per_element_dict[element])
                except KeyError:
                    print({key: value for key, value in window.k_value_per_element_dict.items()})
                    try:
                        K_i = float(window.k_value_per_element_dict[element_line])
                    except KeyError as e:
                        print(f"Error: {e}. K_i not found for element {element_line}.")
                        continue
                    
                    
                counts_data = Path.joinpath(window.subfolder_path,f"{window.prename}{element_line}")
                counts_table = utils.file_to_list(counts_data)
                table_of_smi = np.zeros_like(counts_table)
                #print("Counts table loaded.")
                
                counts_table = np.array(counts_table, dtype=float)
                mask_map = np.array(window.mask, dtype=float)
                if spectrum == "Poli":
                    window.livetime_matrix = np.array(window.livetime_matrix, dtype=float)
                    normalized_counts = counts_table / window.livetime_matrix
                    normalized_counts = np.where(normalized_counts < 80000, normalized_counts, normalized_counts.mean())
                    plt.imshow(normalized_counts, cmap=window.color_of_heatmap, interpolation="nearest")
                    plt.colorbar()
                    plt.savefig(f"normalized{element_line}.png")
                    plt.close()
                    table_of_smi = (counts_table * mask_map) / (window.livetime_matrix * K_i)
                    logging.info(f"meaning livetime matrix: {np.mean(window.livetime_matrix)} and mean of table of smi: {np.mean(table_of_smi)}. K_i: {K_i}. Counts table: {np.mean(counts_table)}")
                elif spectrum == "Mono":
                    counts_table = np.where(counts_table < 10*counts_table.mean(), counts_table, 10*counts_table.mean())
                    plt.imshow(counts_table, cmap=window.color_of_heatmap, interpolation="nearest")
                    plt.colorbar()
                    plt.savefig(f"polyx{element_line}.png")
                    plt.close()
                    table_of_smi = (counts_table * mask_map) / K_i
                utils.output_to_file(table_of_smi,Path.joinpath(window.temporary_folder,f"{element_line}_table_of_smi"))    
                #print("SMi table calculated.")             
                        
                
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
                
                #print("Calculating lambda factor and Ci...")
                
                for i, j in tqdm(indices, desc=f"Processing element: {element_line}..."):
                    sm_value = surface_mass_array_masked[i, j]
                    smi_value = table_of_smi[i, j]
                    try:
                        lambda_factor_value = utils.calculate_lambda_factor(sm_value, int(window.z_number_per_element_dict[element]),float(window.energy_per_element_dict[element]), window.concentration_per_element_dict, line)
                    except KeyError as e:
                        lambda_factor_value = utils.calculate_lambda_factor(sm_value, int(window.z_number_per_element_dict[element_line]),float(window.energy_per_element_dict[element_line]), window.concentration_per_element_dict, line)
                    lambda_factor[i, j] = lambda_factor_value
                    
                    if sm_value > 0 :
                        Ci_table[i, j] = (smi_value)/(lambda_factor_value * sm_value)
                        number += 1                        
                    else:
                        Ci_table[i, j] = 0
                    counter += 1
                
                utils.output_to_file(Ci_table, Path.joinpath(window.temporary_folder, f"{element_line}_Ci_table"))
                utils.output_to_file(lambda_factor, Path.joinpath(window.temporary_folder, f"{element_line}_lambda_factor"))
            
                    
                Ci_table_sum = np.sum(Ci_table[table_of_smi != 0])  
                lambda_factor_sum = np.sum(lambda_factor[table_of_smi != 0])      
                lambda_average_factor = lambda_factor_sum/counter
                Ci_average_factor = Ci_table_sum/counter
                
                a = Ci_table[Ci_table != 0]   
                N = len(a)
                d2 = abs(a - Ci_average_factor)**2  
                var = d2.sum() / (N*(N - 1))
                STD_value = var**0.5
                
                print(f"Ci table sum: {Ci_table_sum:.2e}. Lambda factor sum: {lambda_factor_sum:.2e}")
                print(f"Avg Ci: {Ci_average_factor:.2e}. Avg lambda: {lambda_average_factor:.2e}")
                logging.info(F"AVG ci: {np.mean(Ci_table)}. Avg lambda: {np.mean(lambda_factor)}. avg smi: {np.mean(table_of_smi)}. Avg sm: {np.mean(surface_mass_array)}")
                logging.info(f"How much zeros in Ci table: {np.count_nonzero(Ci_table == 0)}")
                logging.info(f"How much zeros in lambda table: {np.count_nonzero(lambda_factor == 0)}")
                
                
                with open(os.path.join(window.output_path,"average_ci_lambda.txt"), mode='a') as file:
                    file.write(f"{element_line}, Avg Ci:, {Ci_average_factor:.4e}, Avg lambda:, {lambda_average_factor:.4e}, STD:, {STD_value}, surface_mass_ mean:, {surface_mass_array_masked_mean} \n")
                    
                
                for i, j in tqdm(np.ndindex(Ci_table.shape), desc="Ereasing heatpoints..."):
                    if Ci_table[i, j] > 5*float(Ci_average_factor):
                        Ci_table_no_heatpoints[i, j] = Ci_average_factor
                    else:
                        Ci_table_no_heatpoints[i, j] = Ci_table[i, j]
                utils.output_to_file(Ci_table_no_heatpoints, Path.joinpath(window.temporary_folder, f"{element_line}_Ci_table_no_heatpoints"))
                
    print("Quantification finished.")
    QMessageBox.information(window,"Qunatification Completed", "Use arrows to see Ci maps. \nUse 'confirm' button to save data. \nUse 'current subfolder combobox' to continue with next data.")
    window.previous_element_button.clicked.disconnect()
    window.next_element_button.clicked.disconnect()
    window.previous_element_button.clicked.connect(lambda: utils.previous_ci_map(window))
    window.next_element_button.clicked.connect(lambda: utils.next_ci_map(window))
    window.confirm_saving_button.setEnabled(True)
    
