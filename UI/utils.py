import sys
import shutil
import os
import numpy as np
from pathlib import Path
from os.path import exists as file_exists
from PyQt6.QtGui import QPalette, QColor, QIcon, QAction, QPixmap
from PyQt6.QtWidgets import QApplication, QMessageBox
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
import new_window
import mode1
import mode2
import mode3
import start_window
import matplotlib.pyplot as plt
from tqdm import tqdm
import xraylib as xr
import math
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT as NavigationToolbar
import matplotlib.pyplot as plt
import plotly.express as px


def colorbox(window):
    window.color_of_heatmap = str(window.colorbar_combobox.currentText())

def use_for_mask(window):
    window.element_for_mask = str(window.element_name_label.text())
    window.Mask_value_label.setText(window.element_for_mask)
    window.quantify_button.setDisabled(False)

def previous_element_for_mask(window, threshold):
    try:
        window.index_of_element -= 1
        element_for_mask = window.elements_in_subfolder[window.index_of_element]
        print("Element for mask: ", element_for_mask)
        window.element_name_label.setText(element_for_mask)
        
        
        window.mask = mask_creating(element_for_mask, window.output_path, window.subfolder_path, window.prename, threshold, window.color_of_heatmap)
        window.antimask = mask_creating(element_for_mask, window.output_path, window.subfolder_path, window.prename, threshold, window.color_of_heatmap)
        mask_number_of_counts = file_to_list(Path.joinpath(window.output_path, "mask_noc"))
        
        color = window.color_of_heatmap

        figure1, ax1 = plt.subplots()
        canvas1 = FigureCanvas(figure1)
        im1 = ax1.imshow(window.mask, cmap=color, interpolation="nearest")
        plt.colorbar(im1, ax=ax1)

        figure2, ax2 = plt.subplots()
        canvas2 = FigureCanvas(figure2)
        im2 = ax2.imshow(mask_number_of_counts, cmap=color, interpolation="nearest")

        plt.colorbar(im2, ax=ax2)
        canvas1.draw()
        canvas2.draw()

        window.sample_picture_label.setPixmap(canvas1.grab())
        window.sample_picture_label2.setPixmap(canvas2.grab())

    except IndexError:
        print("No previous element.")
               
def next_element_for_mask(window, threshold):
    try:
        window.index_of_element += 1
        element_for_mask = window.elements_in_subfolder[window.index_of_element]
        window.element_name_label.setText(element_for_mask)

        print("Element for mask: ", element_for_mask)
        window.mask = mask_creating(element_for_mask, window.output_path, window.subfolder_path, window.prename, threshold, window.color_of_heatmap)
        window.antimask = mask_creating(element_for_mask, window.output_path, window.subfolder_path, window.prename, threshold, window.color_of_heatmap)
        mask_number_of_counts = file_to_list(Path.joinpath(window.output_path, "mask_noc"))
        
        color = window.color_of_heatmap

        figure1, ax1 = plt.subplots()
        canvas1 = FigureCanvas(figure1)
        im1 = ax1.imshow(window.mask, cmap=color, interpolation="nearest")
        plt.colorbar(im1, ax=ax1)

        figure2, ax2 = plt.subplots()
        canvas2 = FigureCanvas(figure2)
        im2 = ax2.imshow(mask_number_of_counts, cmap=color, interpolation="nearest")

        plt.colorbar(im2, ax=ax2)
        canvas1.draw()
        canvas2.draw()

        window.sample_picture_label.setPixmap(canvas1.grab())
        window.sample_picture_label2.setPixmap(canvas2.grab())

    except IndexError:
        print("No next element.")

 
def next_ci_map(window):
    try:
        window.index_of_element += 1
        element = window.elements_in_subfolder[window.index_of_element]
        window.element_name_label.setText(element)

        print("Ci map of element: ", element)
        Ci_table = file_to_list(Path.joinpath(window.output_path, f"{window.prename}{element}"))
        Ci_table_no_heatpints = file_to_list(Path.joinpath(window.temporary_folder, f"{element}_Ci_table_no_heatpoints"))
        
        
        color = window.color_of_heatmap

        figure1, ax1 = plt.subplots()
        canvas1 = FigureCanvas(figure1)
        im1 = ax1.imshow(Ci_table_no_heatpints, cmap=color, interpolation="nearest")
        plt.colorbar(im1, ax=ax1)

        figure2, ax2 = plt.subplots()
        canvas2 = FigureCanvas(figure2)
        im2 = ax2.imshow(Ci_table, cmap=color, interpolation="nearest")

        plt.colorbar(im2, ax=ax2)
        canvas1.draw()
        canvas2.draw()

        window.sample_picture_label.setPixmap(canvas1.grab())
        window.sample_picture_label2.setPixmap(canvas2.grab())

    except IndexError:
        print("No next element.")
        
def previous_ci_map(window):
    try:
        window.index_of_element -= 1
        element = window.elements_in_subfolder[window.index_of_element]
        
        print("Ci map of element: ", element)
        Ci_table = file_to_list(Path.joinpath(window.output_path, f"{window.prename}{element}"))
        Ci_table_no_heatpints = file_to_list(Path.joinpath(window.temporary_folder, f"{element}_Ci_table_no_heatpoints"))
        
        
        color = window.color_of_heatmap

        figure1, ax1 = plt.subplots()
        canvas1 = FigureCanvas(figure1)
        im1 = ax1.imshow(Ci_table_no_heatpints, cmap=color, interpolation="nearest")
        plt.colorbar(im1, ax=ax1)

        figure2, ax2 = plt.subplots()
        canvas2 = FigureCanvas(figure2)
        im2 = ax2.imshow(Ci_table, cmap=color, interpolation="nearest")

        plt.colorbar(im2, ax=ax2)
        canvas1.draw()
        canvas2.draw()

        window.sample_picture_label.setPixmap(canvas1.grab())
        window.sample_picture_label2.setPixmap(canvas2.grab())

    except IndexError:
        print("No pervious element.")

    
def load_input_files(main_folder_path, inputfile_name, window):
    print("Loading input files... ")
    folder = Path(main_folder_path)
    with folder.joinpath(inputfile_name).open("rt") as elements_file:
        window.k_value_per_element_dict = {}
        window.energy_per_element_dict = {}
        window.z_number_per_element_dict = {}
        for line in elements_file:
            columns = line.strip().split()
            element = columns[1]
            k_value = columns[2]
            energy = columns[3]
            z_number = columns[0]
            window.k_value_per_element_dict[element] = k_value
            window.energy_per_element_dict[element] = energy
            window.z_number_per_element_dict[element] = z_number
    print("Inputfile ready.")
    
def load_zeropeak_file(main_folder_path, zeropeak_coefficients_name, window):
    folder = Path(main_folder_path)
    with folder.joinpath(zeropeak_coefficients_name).open("rt") as zeropeak_factors:
        window.zeropeak_dict = {}
        for line in zeropeak_factors:
            columns = line.strip().split()
            window.zeropeak_dict["a"] = columns[0]
            window.zeropeak_dict["b"] = columns[1]
    print("Zeropeak factors ready.")
    
def load_scatter_file(main_folder_path, scatter_coefficients_name, window):
    folder = Path(main_folder_path)
    with folder.joinpath(main_folder_path, scatter_coefficients_name).open() as scater_factors:
        window.scater_dict = {}
        for line in scater_factors:
            columns = line.strip().split()
            window.scater_dict["a"] = columns[0]
            window.scater_dict["b"] = columns[1]
    print("Scater factors ready.")
    
def load_sample_matrix_file(main_folder_path, sample_matrix_name, window):
    folder = Path(main_folder_path)
    with folder.joinpath(sample_matrix_name).open("rt") as sample_matrix_file:
        window.concentration_per_element_dict = {}
        for line in sample_matrix_file:
            columns = line.strip().split()
            element = columns[0]
            concentration = columns[1]
            window.concentration_per_element_dict[element] = concentration
    print("Sample matrix ready.")
    
def box_folder_changed(window, zeropeak_name, scater_name, spectrum, main_folder_path, treshold):
    window.previous_element_button.setEnabled(True)
    window.next_element_button.setEnabled(True)
    window.previous_element_button.clicked.connect(lambda: previous_element_for_mask(window, treshold))
    window.next_element_button.clicked.connect(lambda: next_element_for_mask(window, treshold))
    current_folder = str(window.prefere_folder_combobox.currentText())
    print(f"Current Folder selected From QCombobox: {current_folder}")
    change_folder(window, main_folder_path, scater_name, zeropeak_name, spectrum, current_folder, treshold)
    
def change_folder(window, main_folder_path, scater_name, zeropeak_name, spectrum, current_folder, treshold):
    window.current_folder_name = current_folder
    window.elements_in_subfolder = []
    window.index_of_element = 0
    current_folder = window.current_folder_name
    print(f"Current Folder selected: {current_folder}")
    main_folder_path = Path(main_folder_path)
    
    window.subfolder_path = Path.joinpath(main_folder_path, current_folder)
    subfolder_insides = os.listdir(window.subfolder_path)
    window.elements_in_subfolder.clear()
    for file in subfolder_insides:
        element_line = file.rsplit("_", 1)[-1].split(".")[0]
        element = element_line.split("-")[0]
        try:
            line = element_line.split("-")[1]
        except Exception as e:
            line = "K"
            print(f"Error: {e}")
        if element not in [scater_name, zeropeak_name]:
            window.elements_in_subfolder.append(element_line)
    prename_ = subfolder_insides[0].rsplit("_", 1)[0]
    window.prename = prename_ + "_"
    print("Folder selected.")
    print("Elements in subfolder: ", window.elements_in_subfolder)
    
    if spectrum == "Poli":
        calculate_livetime(zeropeak_name, window.zeropeak_dict, window)
        output_to_file(window.livetime_matrix, Path.joinpath(window.output_path, f"livetime_map"))
        
    if not Path.joinpath(main_folder_path, f"{current_folder}_output").exists():
        Path.joinpath(main_folder_path, f"{current_folder}_output").mkdir() 
        print("Output folder created.")
        window.output_path = Path.joinpath(main_folder_path, f"{current_folder}_output")
    else:
        window.output_path = Path.joinpath(main_folder_path, f"{current_folder}_output")
        print("Output folder already exists.")
        
    
        
    element_for_mask = window.elements_in_subfolder[window.index_of_element]
    window.element_name_label.setText(element_for_mask)

    
    print("Element for mask: ", element_for_mask)
    window.mask = mask_creating(element_for_mask, window.output_path, window.subfolder_path, window.prename, treshold, window.color_of_heatmap)
    print("Mask map calculated.")
    window.antimask = mask_creating(element_for_mask, window.output_path, window.subfolder_path, window.prename, treshold, window.color_of_heatmap)
    print("Antimask map calculated.")
    mask_number_of_counts = file_to_list(Path.joinpath(window.subfolder_path, f"{window.prename}{element}"))

    figure, ax = plt.subplots()
    canvas = FigureCanvas(figure)
    canvas2 = FigureCanvas(figure)

    im = ax.imshow(window.mask, cmap=window.color_of_heatmap, interpolation="nearest")
    im2 = ax.imshow(mask_number_of_counts, cmap=window.color_of_heatmap, interpolation="nearest")

    canvas.draw()
    canvas2.draw()
    plt.colorbar(im, ax=ax)
    plt.colorbar(im2, ax=ax)
    window.sample_picture_label.setPixmap(canvas.grab())
    window.sample_picture_label2.setPixmap(canvas2.grab())

    
def calculate_livetime(zeropeak_name, zeropeak_dict, window):
    window.zeropeak_matrix = np.array(file_to_list(Path.joinpath(window.subfolder_path, f"{window.prename}{zeropeak_name}")))
    window.livetime_matrix = np.array(LT_calc(window.zeropeak_matrix, float(zeropeak_dict["a"]), float(zeropeak_dict["b"])))
    print("Livetime matrix calculated.")
   
def file_to_list(input):
    """Loads a client file regardless of whether it's .txt or .csv."""
    # Check both possible extensions
    txt_path = os.path.join(input,".txt")
    csv_path = os.path.join(input,".csv")
    
    try:
        if os.path.exists(txt_path):
            with open(input, 'r') as file:
                first_line = file.readline()
                delimiter = ';' if ';' in first_line else ','
            converted_array = np.loadtxt(input, delimiter=delimiter)
            return np.array(converted_array)
        elif os.path.exists(csv_path):
            with open(input, 'r') as file:
                first_line = file.readline()
                delimiter = ';' if ';' in first_line else ','
            converted_array = np.loadtxt(input, delimiter=delimiter)
            return np.array(converted_array)
    except Exception as e:
        print(f"Couldn't find data: {e}")
        print(input)
        return None

def LT_calc(input, a, b):
    if not isinstance(input, np.ndarray):
        raise TypeError(f"Input must be a numpy array. Received: value: {input} with type {type(input)}")
    if not isinstance(a, (int, float)):
        raise TypeError(f"Parameter 'a' must be an int or float. received: value: {a} with type {type(a)}")
    if not isinstance(b, (int, float)):
        raise TypeError(f"Parameter 'b' must be an int or float. Received: value: {b} with type {type(b)}")
    
    return np.array(a * input + b)

def output_to_file(input, output):
    np.savetxt(f"{output}.txt", input, fmt='%.2e', delimiter=',')

def mask_creating(element, output_path, folder_path, prename, treshold, color):
    file_path = Path.joinpath(folder_path, f"{prename}{element}")
    table_of_mask = file_to_list(file_path)
    maxof_masktable = np.max(table_of_mask)
    procent = float(treshold) / 100
    mask = np.where(table_of_mask < (procent * maxof_masktable), 0, 1)

    output_to_file(mask, Path.joinpath(output_path, f"mask"))
    output_to_file(table_of_mask, Path.joinpath(output_path, "mask_noc"))

    plt.imshow(mask, cmap=color, interpolation="nearest")
    plt.title("Mask heatmap")
    plt.savefig(Path.joinpath(output_path, "mask.png"))
    plt.close()

    plt.imshow(table_of_mask, cmap=color, interpolation="nearest")
    plt.title("Mask number of counts")
    plt.colorbar()
    plt.savefig(Path.joinpath(output_path, "mask_noc.png"))
    plt.close()

    return mask

def antimask_creating(element, output_path, folder_path, prename, treshold, color):
    table_of_mask = None
    file_path = Path.joinpath(folder_path, f"{prename}{element}")
    table_of_mask = file_to_list(file_path)
    maxof_masktable = np.max(table_of_mask)
    procent = float(treshold) / 100
    mask = np.where(table_of_mask < (procent * maxof_masktable), 1, 0)

    output_to_file(mask, Path.joinpath(output_path, f"{prename}antimask"))

    plt.imshow(mask, cmap=color, interpolation="nearest")
    plt.title("Antimask heatmap")
    plt.savefig(Path.joinpath(output_path, "antimask.png"))
    plt.close()

    plt.imshow(table_of_mask, cmap=color, interpolation="nearest")
    plt.title("Antimask number of counts")
    plt.colorbar()
    plt.savefig(Path.joinpath(output_path, "antimask_noc.png"))
    plt.close()

    return mask

def SampSM_calc(input, a, b):
    if not isinstance(input, np.ndarray):
        raise TypeError(f"Input must be a numpy array. Received: value: {input} with type {type(input)}")
    if not isinstance(a, (int, float)):
        raise TypeError(f"Parameter 'a' must be an int or float. received: value: {a} with type {type(a)}")
    if not isinstance(b, (int, float)):
        raise TypeError(f"Parameter 'b' must be an int or float. Received: value: {b} with type {type(b)}")
    
    output = np.maximum(a * input + b, 0)
    return output.tolist()

def absorption_coefficient(sample_dict, Ee):
    u_E = 0
    for key, value in sample_dict.items():
        try:
            numeric_value = float(value)
            u_E += xr.CS_Total_CP(key, Ee) * numeric_value
        except ValueError:
            print(f"Non-numeric value encountered for element {key}: {value}")
    return u_E  # jednostka cm^2/g

def calculate_lambda_factor(rho_D, Z, Eeffi, sample_dict):
    """
    Calculate the lambda correction factor for a given element.

    Parameters:
    rho_D (float): Density of the sample.
    Z (int): Atomic number of the element.
    Eeffi (float): Effective energy.
    sample_dict (dict): Dictionary containing the sample composition.

    Returns:
    float: The lambda correction factor.
    """
    phi_in = math.radians(50)
    phi_out = math.radians(50)

    Eijk = xr.LineEnergy(Z, xr.KA1_LINE)
    u_Eijk = absorption_coefficient(sample_dict, Eijk)
    u_Eeffi = absorption_coefficient(sample_dict, Eeffi)

    denominator = rho_D * ((u_Eeffi / math.sin(phi_in)) + (u_Eijk / math.sin(phi_out)))
    if denominator == 0:
        correction_factor = 0
    else:
        numerator = 1 - math.exp(-denominator)
        correction_factor = denominator / numerator
    return correction_factor

##---------------------------Saving---------------------------##
def save_quantification_data(window):
    print("Saving quantification data...")
    for key in window.elements_in_subfolder:
        element = key
        try:
            sm = file_to_list(os.path.join(window.temporary_folder,"sample_mass_noc"))
            table_of_smi = file_to_list(os.path.join(window.temporary_folder,f"{element}_table_of_smi"))
            Ci_table = file_to_list(os.path.join(window.temporary_folder,f"{element}_Ci_table"))
        except Exception as e:
            print(f"Couldn't find data: {e}")
            
            
        if window.element_mass_dat_checkbox.isChecked():
            if window.element_mass_g_checkbox.isChecked():
                SMi_saving_dat(table_of_smi,os.path.join(window.output_path,f"{window.prename}_{element}_smi"),element,1)
            if window.element_mass_mg_checkbox.isChecked():
                SMi_saving_dat(table_of_smi,os.path.join(window.output_path,f"{window.prename}_{element}_smi"),element,1000)
            if window.element_mass_ug_checkbox.isChecked():
                SMi_saving_dat(table_of_smi,os.path.join(window.output_path,f"{window.prename}_{element}_smi"),element,1000000)
            if window.element_mass_ng_checkbox.isChecked():
                SMi_saving_dat(table_of_smi,os.path.join(window.output_path,f"{window.prename}_{element}_smi"),element,1000000000)
                                
        if window.element_mass_png_checkbox.isChecked():
            if window.element_mass_g_checkbox.isChecked():
                SMi_saving_plot(table_of_smi,os.path.join(window.output_path,f"{window.prename}_{element}_smi"),element,window.Pixel_size,window.color_of_heatmap,1,".png")
            if window.element_mass_mg_checkbox.isChecked():
                SMi_saving_plot(table_of_smi,os.path.join(window.output_path,f"{window.prename}_{element}_smi"),element,window.Pixel_size,window.color_of_heatmap,1000,".png")
            if window.element_mass_ug_checkbox.isChecked():
                SMi_saving_plot(table_of_smi,os.path.join(window.output_path,f"{window.prename}_{element}_smi"),element,window.Pixel_size,window.color_of_heatmap,1000000,".png")
            if window.element_mass_ng_checkbox.isChecked():
                SMi_saving_plot(table_of_smi,os.path.join(window.output_path,f"{window.prename}_{element}_smi"),element,window.Pixel_size,window.color_of_heatmap,1000000000,".png")

        if window.element_mass_bmp_checkbox.isChecked():
            if window.element_mass_g_checkbox.isChecked():
                SMi_saving_plot(table_of_smi,os.path.join(window.output_path,f"{window.prename}_{element}_smi"),element,window.Pixel_size,window.color_of_heatmap,1,".pdf")
            if window.element_mass_mg_checkbox.isChecked():
                SMi_saving_plot(table_of_smi,os.path.join(window.output_path,f"{window.prename}_{element}_smi"),element,window.Pixel_size,window.color_of_heatmap,1000,".pdf")
            if window.element_mass_ug_checkbox.isChecked():
                SMi_saving_plot(table_of_smi,os.path.join(window.output_path,f"{window.prename}_{element}_smi"),element,window.Pixel_size,window.color_of_heatmap,1000000,".pdf")
            if window.element_mass_ng_checkbox.isChecked():
                SMi_saving_plot(table_of_smi,os.path.join(window.output_path,f"{window.prename}_{element}_smi"),element,window.Pixel_size,window.color_of_heatmap,1000000000,".pdf")
        
        if window.element_mass_tiff_checkbox.isChecked():
            if window.element_mass_g_checkbox.isChecked():
                SMi_saving_plot(table_of_smi,os.path.join(window.output_path,f"{window.prename}_{element}_smi"),element,window.Pixel_size,window.color_of_heatmap,1,".tiff")
            if window.element_mass_mg_checkbox.isChecked():
                SMi_saving_plot(table_of_smi,os.path.join(window.output_path,f"{window.prename}_{element}_smi"),element,window.Pixel_size,window.color_of_heatmap,1000,".tiff")
            if window.element_mass_ug_checkbox.isChecked():
                SMi_saving_plot(table_of_smi,os.path.join(window.output_path,f"{window.prename}_{element}_smi"),element,window.Pixel_size,window.color_of_heatmap,1000000,".tiff")
            if window.element_mass_ng_checkbox.isChecked():
                SMi_saving_plot(table_of_smi,os.path.join(window.output_path,f"{window.prename}_{element}_smi"),element,window.Pixel_size,window.color_of_heatmap,1000000000,".tiff")
    
        
        if window.Ci_png_checkbox.isChecked():
            if window.Ci_mg_checkbox.isChecked():
                Ci_saving_plot(Ci_table,os.path.join(window.output_path,f"{window.prename}_{element}_Ci"),element,window.Pixel_size,window.color_of_heatmap,1000,".png")
            if window.Ci_ug_checkbox.isChecked():
                Ci_saving_plot(Ci_table,os.path.join(window.output_path,f"{window.prename}_{element}_Ci"),element,window.Pixel_size,window.color_of_heatmap,1000000,".png")
            if window.Ci_procent_checkbox.isChecked():
                Ci_saving_plot(Ci_table,os.path.join(window.output_path,f"{window.prename}_{element}_Ci"),element,window.Pixel_size,window.color_of_heatmap,100,".png")
                    
        if window.Ci_bmp_checkbox.isChecked():
            if window.Ci_mg_checkbox.isChecked():
                Ci_saving_plot(Ci_table,os.path.join(window.output_path,f"{window.prename}_{element}_Ci"),element,window.Pixel_size,window.color_of_heatmap,1000,".pdf")
            if window.Ci_ug_checkbox.isChecked():
                Ci_saving_plot(Ci_table,os.path.join(window.output_path,f"{window.prename}_{element}_Ci"),element,window.Pixel_size,window.color_of_heatmap,1000000,".pdf")
            if window.Ci_procent_checkbox.isChecked():
                Ci_saving_plot(Ci_table,os.path.join(window.output_path,f"{window.prename}_{element}_Ci"),element,window.Pixel_size,window.color_of_heatmap,100,".pdf")
                
        if window.Ci_tiff_checkbox.isChecked():
            if window.Ci_mg_checkbox.isChecked():
                Ci_saving_plot(Ci_table,os.path.join(window.output_path,f"{window.prename}_{element}_Ci"),element,window.Pixel_size,window.color_of_heatmap,1000,".tiff")
            if window.Ci_ug_checkbox.isChecked():
                Ci_saving_plot(Ci_table,os.path.join(window.output_path,f"{window.prename}_{element}_Ci"),element,window.Pixel_size,window.color_of_heatmap,1000000,".tiff")
            if window.Ci_procent_checkbox.isChecked():
                Ci_saving_plot(Ci_table,os.path.join(window.output_path,f"{window.prename}_{element}_Ci"),element,window.Pixel_size,window.color_of_heatmap,100,".tiff")
                
        if window.Ci_dat_checkbox.isChecked():
            if window.Ci_mg_checkbox.isChecked():
                Ci_saving_dat(Ci_table,os.path.join(window.output_path,f"{window.prename}_{element}_Ci"),element,1000)
            if window.Ci_ug_checkbox.isChecked():
                Ci_saving_dat(Ci_table,os.path.join(window.output_path,f"{window.prename}_{element}_Ci"),element,1000000)
            if window.Ci_procent_checkbox.isChecked():
                Ci_saving_dat(Ci_table,os.path.join(window.output_path,f"{window.prename}_{element}_Ci"),element,100)


        if window.sample_mass_dat_checkbox.isChecked():
            if window.sample_mass_g_checkbox.isChecked():
                SM_saving_dat(sm,os.path.join(window.output_path,f"{window.prename}_sm"),1)
            if window.sample_mass_mg_checkbox.isChecked():
                SM_saving_dat(sm,os.path.join(window.output_path,f"{window.prename}_sm"),1000)
            if window.sample_mass_ug_checkbox.isChecked():
                SM_saving_dat(sm,os.path.join(window.output_path,f"{window.prename}_sm"),1000000)
            if window.sample_mass_ng_checkbox.isChecked():
                SM_saving_dat(sm,os.path.join(window.output_path,f"{window.prename}_sm"),1000000000)
                                
        if window.sample_mass_png_checkbox.isChecked():
            if window.sample_mass_g_checkbox.isChecked():
                SM_saving_plot(sm,os.path.join(window.output_path,f"{window.prename}_sm"),window.Pixel_size,window.color_of_heatmap,1,".png")
            if window.sample_mass_mg_checkbox.isChecked():
                SM_saving_plot(sm,os.path.join(window.output_path,f"{window.prename}_sm"),window.Pixel_size,window.color_of_heatmap,1000,".png")
            if window.sample_mass_ug_checkbox.isChecked():
                SM_saving_plot(sm,os.path.join(window.output_path,f"{window.prename}_sm"),window.Pixel_size,window.color_of_heatmap,1000000,".png")
            if window.sample_mass_ng_checkbox.isChecked():
                SM_saving_plot(sm,os.path.join(window.output_path,f"{window.prename}_sm"),window.Pixel_size,window.color_of_heatmap,1000000000,".png")

        if window.sample_mass_bmp_checkbox.isChecked():
            if window.sample_mass_g_checkbox.isChecked():
                SM_saving_plot(sm,os.path.join(window.output_path,f"{window.prename}_sm"),window.Pixel_size,window.color_of_heatmap,1,".pdf")
            if window.sample_mass_mg_checkbox.isChecked():
                SM_saving_plot(sm,os.path.join(window.output_path,f"{window.prename}_sm"),window.Pixel_size,window.color_of_heatmap,1000,".pdf")
            if window.sample_mass_ug_checkbox.isChecked():
                SM_saving_plot(sm,os.path.join(window.output_path,f"{window.prename}_sm"),window.Pixel_size,window.color_of_heatmap,1000000,".pdf")
            if window.sample_mass_ng_checkbox.isChecked():
                SM_saving_plot(sm,os.path.join(window.output_path,f"{window.prename}_sm"),window.Pixel_size,window.color_of_heatmap,1000000000,".pdf")
        
        if window.sample_mass_tiff_checkbox.isChecked():
            if window.sample_mass_g_checkbox.isChecked():
                SM_saving_plot(sm,os.path.join(window.output_path,f"{window.prename}_sm"),window.Pixel_size,window.color_of_heatmap,1,".tiff")
            if window.sample_mass_mg_checkbox.isChecked():
                SM_saving_plot(sm,os.path.join(window.output_path,f"{window.prename}_sm"),window.Pixel_size,window.color_of_heatmap,1000,".tiff")
            if window.sample_mass_ug_checkbox.isChecked():
                SM_saving_plot(sm,os.path.join(window.output_path,f"{window.prename}_sm"),window.Pixel_size,window.color_of_heatmap,1000000,".tiff")
            if window.sample_mass_ng_checkbox.isChecked():
                SM_saving_plot(sm,os.path.join(window.output_path,f"{window.prename}_sm"),window.Pixel_size,window.color_of_heatmap,1000000000,".tiff")

def Ci_saving_dat(input, path, element, size):
    unit = {1000: "_mg_g", 1000000: "_ug_g", 1: "_g_g", 1000000000: "_ng_g"}.get(size, "")
    Ci_table = np.array(input) * size
    output_to_file(Ci_table, f"{path}{unit}")

def SMi_saving_dat(input, path, element, size):
    unit = {1000: "_mg_g", 1000000: "_ug_g", 1: "_g_g", 1000000000: "_ng_g"}.get(size, "")
    SMi_table = np.array(input) * size
    output_to_file(SMi_table, f"{path}{unit}")

def SM_saving_dat(input, path, size):
    unit = {1000: "_mg_g", 1000000: "_ug_g", 1: "_g_g", 1000000000: "_ng_g"}.get(size, "")
    SM_table = np.array(input) * size
    output_to_file(SM_table, f"{path}{unit}")

def Ci_saving_plot(input, path, element, pixel_size, color, size, extention):
    unit = {1000: "_mg_g", 1000000: "_ug_g", 1: "_g_g", 1000000000: "_ng_g"}.get(size, "")
    Ci_table = np.array(input) * size
    width_um, height_um = Ci_table.shape[1], Ci_table.shape[0]
    plt.xlim(0, (width_um * float(pixel_size) / 1000))
    plt.ylim((height_um * float(pixel_size) / 1000), 0)
    plt.imshow(Ci_table, cmap=color, interpolation="nearest")
    plt.title(f"Concentration map of {element} {unit}")
    plt.xlabel('X (mm)')
    plt.ylabel('Y (mm)')
    plt.colorbar()
    plt.savefig(f"{path}{unit}{extention}")
    plt.close()

def SMi_saving_plot(input, path, element, pixel_size, color, size, extention):
    unit = {1000: "_mg_g", 1000000: "_ug_g", 1: "_g_g", 1000000000: "_ng_g"}.get(size, "")
    SMi_table = np.array(input) * size
    width_um, height_um = SMi_table.shape[1], SMi_table.shape[0]
    plt.xlim(0, (width_um * float(pixel_size) / 1000))
    plt.ylim((height_um * float(pixel_size) / 1000), 0)
    plt.imshow(SMi_table, cmap=color, interpolation="nearest")
    plt.title(f"Mass map of element: {element} {unit}")
    plt.xlabel('X (mm)')
    plt.ylabel('Y (mm)')
    plt.colorbar()
    plt.savefig(f"{path}{unit}{extention}")
    plt.close()

def SM_saving_plot(input, path, pixel_size, color, size, extention):
    unit = {1000: "_mg_g", 1000000: "_ug_g", 1: "_g_g", 1000000000: "_ng_g"}.get(size, "")
    SM_table = np.array(input) * size
    width_um, height_um = SM_table.shape[1], SM_table.shape[0]
    plt.xlim(0, (width_um * float(pixel_size) / 1000))
    plt.ylim((height_um * float(pixel_size) / 1000), 0)
    plt.imshow(SM_table, cmap=color, interpolation="nearest")
    plt.title(f"Sample mass map {unit}")
    plt.xlabel('X (mm)')
    plt.ylabel('Y (mm)')
    plt.colorbar()
    plt.savefig(f"{path}{unit}{extention}")
    plt.close()
   