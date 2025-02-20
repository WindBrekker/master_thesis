import numpy as np
import xraylib as xr
import os
import math
import matplotlib.pyplot as plt

def file_to_list(input):
    try:
        converted_array = np.loadtxt(input, delimiter=',')
        return converted_array
    except:
        print("Couldn't find data")
        print(input)
        return None

def LT_calc(input, a, b):
    print (input.shape)
    return (float(a) * input + float(b)).tolist()

def SampSM_calc(input, a, b):
    output = np.maximum(a * input + b, 0)
    return output.tolist()

def output_to_file(input, output):
    np.savetxt(f"{output}.txt", input, fmt='%.2e', delimiter=',')

def absorption_coefficient(sample_dict, Ee):
    u_E = sum(xr.CS_Total_CP(key, Ee) * float(sample_dict[key]) for key in sample_dict)
    return u_E  # jednostka cm^2/g

def lambda_factor(rho_D, Z, Eeffi, sample_dict):
    phi_in = math.radians(50)
    phi_out = math.radians(50)

    Eijk = xr.LineEnergy(Z, xr.KA1_LINE)
    u_Eijk = absorption_coefficient(sample_dict, Eijk)
    u_Eeffi = absorption_coefficient(sample_dict, Eeffi)

    denominator = rho_D * ((u_Eeffi / math.sin(phi_in)) + (u_Eijk / math.sin(phi_out)))
    numerator = 1 - math.exp(-denominator)
    correction_factor = denominator / numerator if denominator != 0 else 0

    return correction_factor

def mask_creating(element, Path, folder, prename, treshold, color, separator):
    file_path = os.path.join(Path, folder, f"{prename}{separator}{element}.txt")
    table_of_mask = file_to_list(file_path)

    maxof_masktable = np.max(table_of_mask)
    procent = float(treshold) / 100
    mask = np.where(table_of_mask < (procent * maxof_masktable), 0, 1)

    output_to_file(mask, os.path.join(Path, f"{folder}_output", f"{prename}_mask"))

    plt.imshow(mask, cmap=color, interpolation="nearest")
    plt.title("Mask heatmap")
    plt.savefig(os.path.join(Path, f"{folder}_output", "mask.png"))
    plt.close()

    plt.imshow(table_of_mask, cmap=color, interpolation="nearest")
    plt.title("Mask number of counts")
    plt.colorbar()
    plt.savefig(os.path.join(Path, f"{folder}_output", "mask_noc.png"))
    plt.close()

    return mask

def antimask_creating(element, Path, folder, prename, treshold, color, separator):
    file_path = os.path.join(Path, folder, f"{prename}{separator}{element}.txt")
    table_of_mask = file_to_list(file_path)

    maxof_masktable = np.max(table_of_mask)
    procent = float(treshold) / 100
    mask = np.where(table_of_mask < (procent * maxof_masktable), 1, 0)

    output_to_file(mask, os.path.join(Path, f"{folder}_output", f"{prename}_antimask"))

    plt.imshow(mask, cmap=color, interpolation="nearest")
    plt.title("Antimask heatmap")
    plt.savefig(os.path.join(Path, f"{folder}_output", "antimask.png"))
    plt.close()

    plt.imshow(table_of_mask, cmap=color, interpolation="nearest")
    plt.title("Antimask number of counts")
    plt.colorbar()
    plt.savefig(os.path.join(Path, f"{folder}_output", "antimask_noc.png"))
    plt.close()

    return mask

def Ci_saving_dat(input, path, element, size):
    unit = {100: "_percent", 1000: "_mg_g", 1000000: "_ug_g"}.get(size, "")
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