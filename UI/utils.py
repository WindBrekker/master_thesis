import sys
import os
import numpy as np
from pathlib import Path
from os.path import exists as file_exists
from PyQt6.QtGui import QPalette, QColor, QIcon, QAction, QPixmap
from PyQt6.QtWidgets import QApplication, QMessageBox
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
import matplotlib.pyplot as plt
import xraylib as xr
import math
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT as NavigationToolbar
import matplotlib.pyplot as plt
import plotly.express as px
import logging

logging.basicConfig(
    filename='quantify.log', 
    level=logging.DEBUG
    )

def colorbox(window):
    window.color_of_heatmap = str(window.colorbar_combobox.currentText())
    
def update_tresh(window):
    window.treshold = window.Treshold.text()
    element_for_mask = window.elements_in_subfolder[window.index_of_element]
    print("Element for mask: ", element_for_mask)
    window.mask = mask_creating(window,element_for_mask, window.output_path, window.subfolder_path, window.prename, window.treshold, window.color_of_heatmap)
    window.antimask = antimask_creating(window,element_for_mask, window.output_path, window.subfolder_path, window.prename, window.treshold, window.color_of_heatmap)
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
    plt.close(figure1)
    plt.close(figure2) 
    
    
def update_figure(window, first_plot, second_plot):
    color = window.color_of_heatmap

    figure1, ax1 = plt.subplots()
    canvas1 = FigureCanvas(figure1)
    im1 = ax1.imshow(first_plot, cmap=color, interpolation="nearest")
    plt.colorbar(im1, ax=ax1)

    figure2, ax2 = plt.subplots()
    canvas2 = FigureCanvas(figure2)
    im2 = ax2.imshow(second_plot, cmap=color, interpolation="nearest")

    plt.colorbar(im2, ax=ax2)
    canvas1.draw()
    canvas2.draw()

    window.sample_picture_label.setPixmap(canvas1.grab())
    window.sample_picture_label2.setPixmap(canvas2.grab())
    plt.close(figure1)
    plt.close(figure2)

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
        
        
        window.mask = mask_creating(window, element_for_mask, window.output_path, window.subfolder_path, window.prename, window.treshold, window.color_of_heatmap)
        window.antimask = antimask_creating(window, element_for_mask, window.output_path, window.subfolder_path, window.prename, window.treshold, window.color_of_heatmap)
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
        
        plt.close(figure1)
        plt.close(figure2)

    except IndexError:
        print("No previous element.")
        window.index_of_element -= 1
               
def next_element_for_mask(window, threshold):
    try:
        window.index_of_element += 1
        element_for_mask = window.elements_in_subfolder[window.index_of_element]
        window.element_name_label.setText(element_for_mask)

        print("Element for mask: ", element_for_mask)
        window.mask = mask_creating(window,element_for_mask, window.output_path, window.subfolder_path, window.prename, window.treshold, window.color_of_heatmap)
        window.antimask = antimask_creating(window,element_for_mask, window.output_path, window.subfolder_path, window.prename, window.treshold, window.color_of_heatmap)
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
        plt.close(figure1)
        plt.close(figure2)

    except IndexError:
        print("No next element.")
        window.index_of_element -= 1

 
def next_ci_map(window):
    try:
        window.index_of_element += 1
        print("Index of element: ", window.index_of_element)
        element = window.elements_in_subfolder[window.index_of_element]
        window.element_name_label.setText(element)

        print("Ci map of element: ", element)
        Ci_table = file_to_list(Path.joinpath(window.temporary_folder, f"{element}_Ci_table"))
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
        plt.close(figure1)
        plt.close(figure2)

    except IndexError:
        print("No next element.")
        window.index_of_element -= 1
        print("Index of element: ", window.index_of_element)
        
def previous_ci_map(window):
    try:
        window.index_of_element -= 1
        print("Index of element: ", window.index_of_element)
        element = window.elements_in_subfolder[window.index_of_element]
        window.element_name_label.setText(element)
        
        
        print("Ci map of element: ", element)
        Ci_table = file_to_list(Path.joinpath(window.temporary_folder, f"{element}_Ci_table"))
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
        plt.close(figure1)
        plt.close(figure2)

    except IndexError:
        print("No pervious element.")
        window.index_of_element -= 1
        print("Index of element: ", window.index_of_element)
        

    
def load_input_files(main_folder_path, inputfile_name, window):
    print("Loading inputfiles... ")
    folder = Path(main_folder_path)
    window.treshold = 10
    if os.path.exists(folder.joinpath(inputfile_name + ".txt")):
        inputfile_name = inputfile_name + ".txt"
        #print(f"{folder.joinpath(inputfile_name)} found.")
    elif os.path.exists(folder.joinpath(inputfile_name + ".csv")):
        inputfile_name = inputfile_name + ".csv"
        #print(f"{folder.joinpath(inputfile_name)} found.")
    else:
        raise FileNotFoundError(f"File not found: {folder.joinpath(inputfile_name + ".txt")} or {folder.joinpath(inputfile_name + ".csv")}")
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
            #print(f"Element: {element}, K-value: {k_value}, Energy: {energy}, Z-number: {z_number}")
    print("Inputfile ready.")
    
def load_zeropeak_file(main_folder_path, zeropeak_coefficients_name, window):
    folder = Path(main_folder_path)
    if os.path.exists(folder.joinpath(zeropeak_coefficients_name + ".txt")):
        zeropeak_coefficients_name = zeropeak_coefficients_name + ".txt"
    elif os.path.exists(folder.joinpath(zeropeak_coefficients_name + ".csv")):
        zeropeak_coefficients_name = zeropeak_coefficients_name + ".csv"
    else:
        raise FileNotFoundError(f"File not found: {zeropeak_coefficients_name}.txt or {zeropeak_coefficients_name}.csv")
    with folder.joinpath(zeropeak_coefficients_name).open("rt") as zeropeak_factors:
        window.zeropeak_dict = {}
        for line in zeropeak_factors:
            columns = line.strip().split()
            window.zeropeak_dict["a"] = columns[0]
            window.zeropeak_dict["b"] = columns[1]
    print("Zeropeak factors ready.")
    
def load_scatter_file(main_folder_path, scatter_coefficients_name, window):
    folder = Path(main_folder_path)
    if os.path.exists(folder.joinpath(scatter_coefficients_name + ".txt")):
        scatter_coefficients_name = scatter_coefficients_name + ".txt"
        print(f"reading {scatter_coefficients_name} file")
    elif os.path.exists(folder.joinpath(scatter_coefficients_name + ".csv")):
        scatter_coefficients_name = scatter_coefficients_name + ".csv"
        print(f"reading {scatter_coefficients_name} file")
    else:
        raise FileNotFoundError(f"File not found: {scatter_coefficients_name}.txt or {scatter_coefficients_name}.csv")
    
    with folder.joinpath(main_folder_path, scatter_coefficients_name).open() as scater_factors:
        window.scater_dict = {}
        for line in scater_factors:
            columns = line.strip().split()
            window.scater_dict["a"] = columns[0]
            window.scater_dict["b"] = columns[1]
    print("Scater factors ready.")
    
def load_sample_matrix_file(main_folder_path, sample_matrix_name, window):
    folder = Path(main_folder_path)
    if os.path.exists(folder.joinpath(sample_matrix_name + ".txt")):
        sample_matrix_name = sample_matrix_name + ".txt"
    elif os.path.exists(folder.joinpath(sample_matrix_name + ".csv")):
        sample_matrix_name = sample_matrix_name + ".csv"
    else:
        raise FileNotFoundError(f"File not found: {sample_matrix_name}.txt or {sample_matrix_name}.csv")
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
    window.previous_element_button.clicked.disconnect()
    window.next_element_button.clicked.disconnect()
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
        print("File in subfolder: ", file)
        element_line = file.rsplit("_", 1)[-1].split(".")[0]
        #print("Element line: ", element_line)
        element = element_line.split("-")[0]
        #print("Element: ", element)
        try:
            line = element_line.split("-")[1]
            #print("Line: ", line)
        except Exception as e:
            line = "K"
            print(f"Error with line: {e}")
        if element not in [scater_name, zeropeak_name]:
            window.elements_in_subfolder.append(element_line)
    prename_ = subfolder_insides[0].rsplit("_", 1)[0]
    window.prename = prename_ + "_"
    print("Folder selected.")
    print("Elements in subfolder: ", window.elements_in_subfolder)
    
    
    if not Path.joinpath(main_folder_path, f"{current_folder}_output").exists():
        Path.joinpath(main_folder_path, f"{current_folder}_output").mkdir() 
        #print("Output folder created.")
    else:
        print("Output folder already exists.")
    window.output_path = Path.joinpath(main_folder_path, f"{current_folder}_output")
    
    if spectrum == "Poli":
        calculate_livetime(zeropeak_name, window.zeropeak_dict, window)
        output_to_file(window.livetime_matrix, Path.joinpath(window.output_path, f"livetime_map"))
        
        
    
        
    element_for_mask = window.elements_in_subfolder[window.index_of_element]
    window.element_name_label.setText(element_for_mask)

    
    #print("Element for mask: ", element_for_mask)
    window.mask = mask_creating(window,element_for_mask, window.output_path, window.subfolder_path, window.prename, treshold, window.color_of_heatmap)
    print("Mask map calculated.")
    window.antimask = antimask_creating(window,element_for_mask, window.output_path, window.subfolder_path, window.prename, treshold, window.color_of_heatmap)
    print("Antimask map calculated.")
    
    mask_number_of_counts = file_to_list(Path.joinpath(window.subfolder_path, f"{window.prename}{element_for_mask}"))

    # figure, ax = plt.subplots()
    # canvas = FigureCanvas(figure)
    # canvas2 = FigureCanvas(figure)

    # im = ax.imshow(window.mask, cmap=window.color_of_heatmap, interpolation="nearest")
    # im2 = ax.imshow(mask_number_of_counts, cmap=window.color_of_heatmap, interpolation="nearest")

    # canvas.draw()
    # canvas2.draw()
    # plt.colorbar(im, ax=ax)
    # plt.colorbar(im2, ax=ax)
    # window.sample_picture_label.setPixmap(canvas.grab())
    # window.sample_picture_label2.setPixmap(canvas2.grab())
    # plt.close(figure)
    
    
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
    plt.close(figure1)
    plt.close(figure2)
    
    
    window.Treshold.editingFinished.connect(lambda: update_tresh(window))

    
def calculate_livetime(zeropeak_name, zeropeak_dict, window):
    try:
        window.zeropeak_matrix = np.array(file_to_list(Path.joinpath(window.subfolder_path, f"{window.prename}{zeropeak_name}")))
    except Exception as e:
        print(f"Couldn't find data {Path.joinpath(window.subfolder_path, f"{window.prename}{zeropeak_name}")}: {e}")
    try:
        #window.livetime_matrix = np.array(LT_calc(window.zeropeak_matrix, float(zeropeak_dict["a"]), float(zeropeak_dict["b"])))
        window.livetime_matrix = np.array(LT_calc(window.zeropeak_matrix, float(0), float(0.02)))
        #window.livetime_matrix = window.livetime_matrix * 0.001 # Convert to milliseconds
        print("Livetime matrix calculated.")
        print(window.livetime_matrix)
    except Exception as e:
        print(f"Couldn't calculate livetime matrix: {e}")
        print(f"Zeropeak dict type: {type(zeropeak_dict["a"])}, b: {type(zeropeak_dict["b"])}")
        print(f"Zeropeak matrix type: {type(window.zeropeak_matrix)}")
        print(f"Zeropeak matrix: {window.zeropeak_matrix}")
        print(f"Zeropeak dict: {zeropeak_dict}")
        
        
def file_to_list(input):
    """Loads a client file regardless of whether it's .txt or .csv."""
    # Check both possible extensions
    txt_path = input.with_suffix(".txt")
    #print(f"txt_path: {txt_path}")
    csv_path = input.with_suffix(".csv")
    #print(f"csv_path: {csv_path}")
    
    try:
        if os.path.exists(txt_path):
            with open(txt_path, 'r') as file:
                first_line = file.readline()
                delimiter = ';' if ';' in first_line else ','
            converted_array = np.loadtxt(txt_path, delimiter=delimiter)
            return np.array(converted_array)
        elif os.path.exists(csv_path):
            with open(csv_path, 'r') as file:
                first_line = file.readline()
                delimiter = ';' if ';' in first_line else ','
            converted_array = np.loadtxt(csv_path, delimiter=delimiter)
            converted_array = np.fliplr(converted_array)  # Flip the array horizontally
            return np.array(converted_array)
        else:
            print(f"File not found: {txt_path} or {csv_path}")
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
    
    return np.array((a * input) + b)

def output_to_file(input, output):
    np.savetxt(f"{output}.txt", input, fmt='%.2e', delimiter=',')

def mask_creating(window, element, output_path, folder_path, prename, treshold, color):
    file_path = Path.joinpath(folder_path, f"{prename}{element}")
    table_of_mask = file_to_list(file_path)
    maxof_masktable = np.max(table_of_mask)
    procent = float(window.treshold) / 100
    mask = np.where(table_of_mask < (procent * maxof_masktable), 0, 1)
    logging.info(f"Mask file path: {file_path} and average: {np.mean(table_of_mask)}")
    logging.info(f"Mask mean: {np.mean(mask)}")
    

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


def antimask_creating(window, element, output_path, folder_path, prename, treshold, color):
    file_path = Path.joinpath(folder_path, f"{prename}{element}")
    table_of_mask = file_to_list(file_path)
    maxof_masktable = np.max(table_of_mask)
    procent = float(window.treshold) / 100
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
    logging.info(f"Sample mass calculation: a: {a}, b: {b}. output mean: {np.mean(output)}")
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

def calculate_lambda_factor(rho_D, Z, Eeffi, sample_dict, line):
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

    if line == "K" or line == "Ka":
        Eijk = xr.LineEnergy(Z, xr.KA1_LINE)
    elif line == "Kb":
        Eijk = xr.LineEnergy(Z, xr.KB1_LINE)
    elif line == "La" or line == "L":
        Eijk = xr.LineEnergy(Z, xr.LA1_LINE)
    elif line == "Lb":
        Eijk = xr.LineEnergy(Z, xr.LB1_LINE)
    elif line == "M":
        Eijk = xr.LineEnergy(Z, xr.MA1_LINE)
    else:
        print("Line not recognized.")
        sys.exit()
    u_Eijk = absorption_coefficient(sample_dict, Eijk)
    u_Eeffi = absorption_coefficient(sample_dict, Eeffi)

    denominator = rho_D * ((u_Eeffi / math.sin(phi_in)) + (u_Eijk / math.sin(phi_out)))
    if denominator == 0:
        correction_factor = 0
    else:
        numerator = 1 - math.exp(-denominator)
        correction_factor = numerator/denominator
    return correction_factor

##---------------------------Saving---------------------------##
def save_quantification_data(window):
    print("Saving quantification data...")
    for key in window.elements_in_subfolder:
        element = key
        try:
            sm = file_to_list(Path.joinpath(window.temporary_folder,"sample_mass_noc"))
            table_of_smi = file_to_list(Path.joinpath(window.temporary_folder,f"{element}_table_of_smi"))
            Ci_table = file_to_list(Path.joinpath(window.temporary_folder,f"{element}_Ci_table"))
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
                SMi_saving_plot(table_of_smi,os.path.join(window.output_path,f"{window.prename}_{element}_smi"),element,window.pixel_size,window.color_of_heatmap,1,".png")
            if window.element_mass_mg_checkbox.isChecked():
                SMi_saving_plot(table_of_smi,os.path.join(window.output_path,f"{window.prename}_{element}_smi"),element,window.pixel_size,window.color_of_heatmap,1000,".png")
            if window.element_mass_ug_checkbox.isChecked():
                SMi_saving_plot(table_of_smi,os.path.join(window.output_path,f"{window.prename}_{element}_smi"),element,window.pixel_size,window.color_of_heatmap,1000000,".png")
            if window.element_mass_ng_checkbox.isChecked():
                SMi_saving_plot(table_of_smi,os.path.join(window.output_path,f"{window.prename}_{element}_smi"),element,window.pixel_size,window.color_of_heatmap,1000000000,".png")

        if window.element_mass_bmp_checkbox.isChecked():
            if window.element_mass_g_checkbox.isChecked():
                SMi_saving_plot(table_of_smi,os.path.join(window.output_path,f"{window.prename}_{element}_smi"),element,window.pixel_size,window.color_of_heatmap,1,".pdf")
            if window.element_mass_mg_checkbox.isChecked():
                SMi_saving_plot(table_of_smi,os.path.join(window.output_path,f"{window.prename}_{element}_smi"),element,window.pixel_size,window.color_of_heatmap,1000,".pdf")
            if window.element_mass_ug_checkbox.isChecked():
                SMi_saving_plot(table_of_smi,os.path.join(window.output_path,f"{window.prename}_{element}_smi"),element,window.pixel_size,window.color_of_heatmap,1000000,".pdf")
            if window.element_mass_ng_checkbox.isChecked():
                SMi_saving_plot(table_of_smi,os.path.join(window.output_path,f"{window.prename}_{element}_smi"),element,window.pixel_size,window.color_of_heatmap,1000000000,".pdf")
        
        if window.element_mass_tiff_checkbox.isChecked():
            if window.element_mass_g_checkbox.isChecked():
                SMi_saving_plot(table_of_smi,os.path.join(window.output_path,f"{window.prename}_{element}_smi"),element,window.pixel_size,window.color_of_heatmap,1,".tiff")
            if window.element_mass_mg_checkbox.isChecked():
                SMi_saving_plot(table_of_smi,os.path.join(window.output_path,f"{window.prename}_{element}_smi"),element,window.pixel_size,window.color_of_heatmap,1000,".tiff")
            if window.element_mass_ug_checkbox.isChecked():
                SMi_saving_plot(table_of_smi,os.path.join(window.output_path,f"{window.prename}_{element}_smi"),element,window.pixel_size,window.color_of_heatmap,1000000,".tiff")
            if window.element_mass_ng_checkbox.isChecked():
                SMi_saving_plot(table_of_smi,os.path.join(window.output_path,f"{window.prename}_{element}_smi"),element,window.pixel_size,window.color_of_heatmap,1000000000,".tiff")
    
        
        if window.Ci_png_checkbox.isChecked():
            if window.Ci_mg_checkbox.isChecked():
                Ci_saving_plot(Ci_table,os.path.join(window.output_path,f"{window.prename}_{element}_Ci"),element,window.pixel_size,window.color_of_heatmap,1000,".png")
            if window.Ci_ug_checkbox.isChecked():
                Ci_saving_plot(Ci_table,os.path.join(window.output_path,f"{window.prename}_{element}_Ci"),element,window.pixel_size,window.color_of_heatmap,1000000,".png")
            if window.Ci_procent_checkbox.isChecked():
                Ci_saving_plot(Ci_table,os.path.join(window.output_path,f"{window.prename}_{element}_Ci"),element,window.pixel_size,window.color_of_heatmap,100,".png")
                    
        if window.Ci_bmp_checkbox.isChecked():
            if window.Ci_mg_checkbox.isChecked():
                Ci_saving_plot(Ci_table,os.path.join(window.output_path,f"{window.prename}_{element}_Ci"),element,window.pixel_size,window.color_of_heatmap,1000,".pdf")
            if window.Ci_ug_checkbox.isChecked():
                Ci_saving_plot(Ci_table,os.path.join(window.output_path,f"{window.prename}_{element}_Ci"),element,window.pixel_size,window.color_of_heatmap,1000000,".pdf")
            if window.Ci_procent_checkbox.isChecked():
                Ci_saving_plot(Ci_table,os.path.join(window.output_path,f"{window.prename}_{element}_Ci"),element,window.pixel_size,window.color_of_heatmap,100,".pdf")
                
        if window.Ci_tiff_checkbox.isChecked():
            if window.Ci_mg_checkbox.isChecked():
                Ci_saving_plot(Ci_table,os.path.join(window.output_path,f"{window.prename}_{element}_Ci"),element,window.pixel_size,window.color_of_heatmap,1000,".tiff")
            if window.Ci_ug_checkbox.isChecked():
                Ci_saving_plot(Ci_table,os.path.join(window.output_path,f"{window.prename}_{element}_Ci"),element,window.pixel_size,window.color_of_heatmap,1000000,".tiff")
            if window.Ci_procent_checkbox.isChecked():
                Ci_saving_plot(Ci_table,os.path.join(window.output_path,f"{window.prename}_{element}_Ci"),element,window.pixel_size,window.color_of_heatmap,100,".tiff")
                
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
                SM_saving_plot(sm,os.path.join(window.output_path,f"{window.prename}_sm"),window.pixel_size,window.color_of_heatmap,1,".png")
            if window.sample_mass_mg_checkbox.isChecked():
                SM_saving_plot(sm,os.path.join(window.output_path,f"{window.prename}_sm"),window.pixel_size,window.color_of_heatmap,1000,".png")
            if window.sample_mass_ug_checkbox.isChecked():
                SM_saving_plot(sm,os.path.join(window.output_path,f"{window.prename}_sm"),window.pixel_size,window.color_of_heatmap,1000000,".png")
            if window.sample_mass_ng_checkbox.isChecked():
                SM_saving_plot(sm,os.path.join(window.output_path,f"{window.prename}_sm"),window.pixel_size,window.color_of_heatmap,1000000000,".png")

        if window.sample_mass_bmp_checkbox.isChecked():
            if window.sample_mass_g_checkbox.isChecked():
                SM_saving_plot(sm,os.path.join(window.output_path,f"{window.prename}_sm"),window.pixel_size,window.color_of_heatmap,1,".pdf")
            if window.sample_mass_mg_checkbox.isChecked():
                SM_saving_plot(sm,os.path.join(window.output_path,f"{window.prename}_sm"),window.pixel_size,window.color_of_heatmap,1000,".pdf")
            if window.sample_mass_ug_checkbox.isChecked():
                SM_saving_plot(sm,os.path.join(window.output_path,f"{window.prename}_sm"),window.pixel_size,window.color_of_heatmap,1000000,".pdf")
            if window.sample_mass_ng_checkbox.isChecked():
                SM_saving_plot(sm,os.path.join(window.output_path,f"{window.prename}_sm"),window.pixel_size,window.color_of_heatmap,1000000000,".pdf")
        
        if window.sample_mass_tiff_checkbox.isChecked():
            if window.sample_mass_g_checkbox.isChecked():
                SM_saving_plot(sm,os.path.join(window.output_path,f"{window.prename}_sm"),window.pixel_size,window.color_of_heatmap,1,".tiff")
            if window.sample_mass_mg_checkbox.isChecked():
                SM_saving_plot(sm,os.path.join(window.output_path,f"{window.prename}_sm"),window.pixel_size,window.color_of_heatmap,1000,".tiff")
            if window.sample_mass_ug_checkbox.isChecked():
                SM_saving_plot(sm,os.path.join(window.output_path,f"{window.prename}_sm"),window.pixel_size,window.color_of_heatmap,1000000,".tiff")
            if window.sample_mass_ng_checkbox.isChecked():
                SM_saving_plot(sm,os.path.join(window.output_path,f"{window.prename}_sm"),window.pixel_size,window.color_of_heatmap,1000000000,".tiff")


    print("Quantification data saved.")
    
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
    unit = {1000: "_mg_cm2", 1000000: "_ug_cm2", 1: "_g_cm2", 1000000000: "_ng_cm2"}.get(size, "")
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
   