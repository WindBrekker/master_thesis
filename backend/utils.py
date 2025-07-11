import os
import numpy as np
import utils
from pathlib import Path
import matplotlib.pyplot as plt
from tqdm import tqdm
import xraylib as xr
import math



def file_to_list(input):
    try:
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
    table_of_mask = None
    while table_of_mask is None:
        element = input("Enter the element for mask creation: ")
        file_path = Path.joinpath(folder_path, f"{prename}{element}-K.csv")
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
    while table_of_mask is None:
        element = input("Enter the element for ANTImask creation: ")
        file_path = Path.joinpath(folder_path, f"{prename}{element}-K.csv")
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

def Ci_saving_dat(input, path, element, size):
    unit = {100: "_percent", 1000: "_mg_g", 1000000: "_ug_g"}.get(size, "")
    Ci_table = np.array(input) * size
    output_to_file(Ci_table, f"{path}{element}{unit}")

def SMi_saving_dat(input, path, element, size):
    unit = {1000: "_mg_g", 1000000: "_ug_g", 1: "_g_g", 1000000000: "_ng_g"}.get(size, "")
    SMi_table = np.array(input) * size
    output_to_file(SMi_table, f"{path}{unit}")

def SM_saving_dat(input, path, size):
    unit = {1000: "_mg_g", 1000000: "_ug_g", 1: "_g_g", 1000000000: "_ng_g"}.get(size, "")
    print(unit)
    print(size)
    SM_table = np.array(input) * size
    output_to_file(SM_table, f"{path}{unit}")

def Ci_saving_plot(input, path, element, pixel_size, color, size, extention):
    unit = {100: "_percent", 1000: "_mg_g", 1000000: "_ug_g"}.get(size, "")
    Ci_table = np.array(input) * size
    width_um, height_um = Ci_table.shape[1], Ci_table.shape[0]
    plt.xlim(0, (width_um * float(pixel_size) / 1000))
    plt.ylim((height_um * float(pixel_size) / 1000), 0)
    plt.imshow(Ci_table, cmap=color, interpolation="nearest")
    plt.title(f"Concentration map of {element} {unit}")
    plt.xlabel('X (mm)')
    plt.ylabel('Y (mm)')
    plt.colorbar()
    plt.savefig(Path.joinpath(path, f"{element}{unit}{extention}"))
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
   