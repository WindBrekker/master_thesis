import os
import numpy as np
import utils
from pathlib import Path
import matplotlib.pyplot as plt
from tqdm import tqdm
import xraylib as xr
import math

def get_input(prompt, default=None):
    user_input = input(f"{prompt} [{default}]: ")
    return user_input if user_input else default

def main():
    print("Welcome to QuantumSlice")

    # Get user inputs
    main_folder = get_input("Enter the path to the main folder")
    main_folder_path = Path(main_folder)
    pixel_size =  1000
    inputfile_name = "inputfile"
    zeropeak_name = "zeropeak"
    scater_name ="scater"
    sample_matrix_name = "sample_matrix"
    treshold = 10
    color_of_heatmap ="jet"
    zeropeak_coefficients = "zeropeak_coefficients"
    scater_coefficients = "scater_coefficients"

    print("Loading input files... ")
    with open(Path.joinpath(main_folder_path, f"{inputfile_name}.txt"), "rt") as elements_file:
        k_value_per_element_dict = {}
        energy_per_element_dict = {}
        z_number_per_element_dict = {}
        for line in elements_file:
            columns = line.strip().split()
            element = columns[1]
            k_value = columns[2]
            energy = columns[3]
            z_number = columns[0]
            k_value_per_element_dict[element] = k_value
            energy_per_element_dict[element] = energy
            z_number_per_element_dict[element] = z_number
    print("Inputfile ready.")
    
    with open(Path.joinpath(main_folder_path, f"{scater_coefficients}.txt")) as scater_factors:
        scater_dict = {}
        for line in scater_factors:
            columns = line.strip().split()
            scater_dict["a"] = columns[0]
            scater_dict["b"] = columns[1]
    print("Scater factors ready.")

    with open(Path.joinpath(main_folder_path, f"{zeropeak_coefficients}.txt")) as zeropeak_factors:
        zeropeak_dict = {}
        for line in zeropeak_factors:
            columns = line.strip().split()
            zeropeak_dict["a"] = columns[0]
            zeropeak_dict["b"] = columns[1]
    print("Zeropeak factors ready.")

    with open(Path.joinpath(main_folder_path, f"{sample_matrix_name}.txt"), "rt" ) as sample_matrix_file:
        concentration_per_element_dict = {}
        for line in sample_matrix_file:
            columns = line.strip().split()
            element = columns[0]
            concentration = columns[1]
            concentration_per_element_dict[element] = concentration
    print("Sample matrix ready.")

    # List folders in the main directory
    main_folder_insides = os.listdir(main_folder_path)
    folders_names = [file for file in main_folder_insides if os.path.isdir(Path.joinpath(main_folder_path, file)) and not file.endswith("_output")]

    # Select a folder
    current_folder = folders_names[0]
    elements_in_subfolder = []

    # List elements and prename in the folder
    subfolder_path = Path.joinpath(main_folder_path, current_folder)
    subfolder_insides = os.listdir(subfolder_path)
    elements_in_subfolder.clear()
    for file in subfolder_insides:
        element = file.rsplit("_", 1)[-1].split(".")[0]
        if element not in [scater_name, zeropeak_name]:
            elements_in_subfolder.append(element)
    prename = subfolder_insides[0].rsplit("_", 1)[0]
    prename = prename + "_"
    print("Folder selected.")
 
    # Calculate livetime with zeropeak
    zeropeak_matrix = np.array(utils.file_to_list(Path.joinpath(subfolder_path, f"{prename}{zeropeak_name}.txt")))
    livetime_matrix = np.array(utils.LT_calc(zeropeak_matrix, float(zeropeak_dict["a"]), float(zeropeak_dict["b"])))
    print("Livetime matrix calculated.")

    if not Path.joinpath(main_folder_path, f"{current_folder}_output").exists():
        Path.joinpath(main_folder_path, f"{current_folder}_output").mkdir() 
    output_path = Path.joinpath(main_folder_path, f"{current_folder}_output")
    print("Output folder created.")

    utils.output_to_file(livetime_matrix, Path.joinpath(output_path, f"{prename}livetime_map"))
       
    element_for_mask = None
    mask_map = utils.mask_creating(element_for_mask, output_path, subfolder_path, prename, treshold, color_of_heatmap)
    print("Mask map calculated.")
    
    antimask_map = utils.antimask_creating(element_for_mask, output_path, subfolder_path, prename,   treshold, color_of_heatmap)
    print("Antimask map calculated.")

    # Display mask images
    plt.imshow(mask_map, cmap=color_of_heatmap, interpolation="nearest")
    plt.title("Mask heatmap")
    plt.savefig(Path.joinpath(output_path, "mask.png"))
    plt.show()

    
    picture = utils.file_to_list(Path.joinpath(output_path, "mask_noc.txt"))
    picture = np.array(picture, dtype=float)
    
    
    plt.imshow(picture, cmap=color_of_heatmap, interpolation="nearest")
    plt.title("Mask number of counts")
    plt.colorbar()
    plt.savefig(Path.joinpath(main_folder_path, f"{current_folder}_output", "mask_noc.png"))
    plt.show()
    
    print("Ready to quantify elements.")

    # Quantify elements
    for folder in folders_names:
        current_folder = folder
        subfolder_path = Path.joinpath(main_folder_path, current_folder)
        subfolder_insides = os.listdir(subfolder_path)
        elements_in_subfolder.clear()
        for file in subfolder_insides:
            element = file.rsplit("_", 1)[-1].split(".")[0]
            if element not in [scater_name, zeropeak_name]:
                elements_in_subfolder.append(element)
        print(f"Processing folder: {current_folder}. Found elements: {elements_in_subfolder}")
        file_names = os.listdir(Path.joinpath(main_folder_path, folder))
        first_file = file_names[0]
        splitted_prename = first_file.rsplit("_", 1)
        prename = splitted_prename[0]
        prename = prename + "_"
        separator = "_"

        # Calculate livetime with zeropeak
        zeropeak_matrix = np.array(utils.file_to_list(Path.joinpath(subfolder_path, f"{prename}{zeropeak_name}.txt")))
        livetime_matrix = np.array(utils.LT_calc(zeropeak_matrix, float(zeropeak_dict["a"]), float(zeropeak_dict["b"])))
        print("Livetime matrix calculated.")

        if not Path.joinpath(main_folder_path, f"{current_folder}_output").exists():
            Path.joinpath(main_folder_path, f"{current_folder}_output").mkdir() 
        output_path = Path.joinpath(main_folder_path, f"{current_folder}_output")
        print("Output folder created.")
        
        utils.output_to_file(livetime_matrix, Path.joinpath(output_path, f"livetime_map"))
        element_for_mask = None
        mask_map = utils.mask_creating(element_for_mask, output_path, subfolder_path, prename, treshold, color_of_heatmap)
        print("Mask map calculated.")
        antimask_map = utils.antimask_creating(element_for_mask, output_path, subfolder_path, prename, treshold, color_of_heatmap)
        print("Antimask map calculated.")

        # Create folder for outputs
        if not Path.joinpath(main_folder_path, "temporary").exists():
            Path.joinpath(main_folder_path, "temporary").mkdir()
        if not Path.joinpath(main_folder_path, "temporary", f"{folder}_output").exists():
            Path.joinpath(main_folder_path, "temporary", f"{folder}_output").mkdir()
        temporary_folder = Path.joinpath(main_folder_path, "temporary", f"{folder}_output")
        print("temporary folder created.")
        
        scater_tab = np.array(utils.file_to_list(Path.joinpath(subfolder_path, f"{prename}{scater_name}.txt")))
        scater_tab = scater_tab/livetime_matrix
        print("Scater table calculated.")
            
        # Create arrays for calculations
        surface_mass_array = []
        sample_mass_livetime = np.zeros_like(scater_tab)
        antimask_scater = np.zeros_like(scater_tab)
        antimask_scater_mask = np.zeros_like(scater_tab)
        antimask_scater_masked = np.zeros_like(scater_tab)

        antimask_scater = scater_tab * antimask_map

        scater_treshold = np.min(scater_tab)
        
        antimask_scater_mask = (antimask_map & (antimask_scater < (1.25 * scater_treshold))).astype(int)

        utils.output_to_file(antimask_scater_mask, Path.joinpath(temporary_folder, "antimask_scater_mask"))
        
        print("Antimask scater mask calculated.")
        
        antimask_scater_masked = antimask_scater * antimask_scater_mask
        antimask_sum = np.sum(antimask_scater_masked)
        iteration_antimask = np.count_nonzero(antimask_scater_mask)
        
        antimask_mean = np.mean(antimask_scater_masked[antimask_scater_masked != 0]) if iteration_antimask != 0 else 0

        plt.imshow(antimask_scater_mask, cmap=color_of_heatmap, interpolation="nearest")
        plt.savefig("antimask_plot.png")

        difference = scater_tab - float(antimask_mean)


        sample_mass_livetime = np.where(difference > 0, difference, 0)
        surface_mass_array = np.array(utils.SampSM_calc(sample_mass_livetime, float(scater_dict["a"]), float(scater_dict["b"])))
        surface_mass_array_masked = np.multiply(surface_mass_array, mask_map)
        
        utils.output_to_file(surface_mass_array_masked, Path.joinpath(temporary_folder, "sample_mass_noc"))
        print("Sample mass calculated.")

        #loop for every element in all folders
        for key in z_number_per_element_dict:
                element = key
                print(f"Processing element: {element} ...")
                
                #check if there is data for the element in this folder
                if Path.joinpath(subfolder_path, f"{prename}{element}.txt").exists():
                    K_i = float(k_value_per_element_dict[element])
                    counts_data = Path.joinpath(subfolder_path,f"{prename}{element}.txt")
                    counts_table = utils.file_to_list(counts_data)
                    table_of_smi = np.zeros_like(counts_table)
                    print("Counts table loaded.")
                    
                    counts_table = np.array(counts_table, dtype=float)
                    mask_map = np.array(mask_map, dtype=float)
                    livetime_matrix = np.array(livetime_matrix, dtype=float)
                    table_of_smi = (counts_table * mask_map) / livetime_matrix / K_i
                    utils.output_to_file(table_of_smi,Path.joinpath(temporary_folder,f"{element}_table_of_smi"))    
                    print("SMi table calculated.")             
                            
                    

                    Ci_table = np.zeros_like(table_of_smi)
                    Ci_table_no_heatpoints = np.zeros_like(table_of_smi)
                    lambda_factor = np.zeros_like(table_of_smi)
                    median_value = np.median(surface_mass_array)
                    total_elements = surface_mass_array.size
                    indices = np.argwhere(table_of_smi != 0)
                    
                    counter = 0
                    number = 0
                    Ci_table_sum = 0
                    lambda_factor_sum = 0
                    
                    print("Calculating lambda factor and Ci...")
                    
                    for i, j in tqdm(indices, desc="Processing elements"):
                        value = surface_mass_array[i, j]
                        smi_value = table_of_smi[i, j]
                        lambda_factor_value = utils.calculate_lambda_factor(value, int(z_number_per_element_dict[element]),float(energy_per_element_dict[element]), concentration_per_element_dict )
                        lambda_factor[i, j] = lambda_factor_value
                        
                        if value > 0.3 * median_value and smi_value >= 0:
                            Ci_table[i, j] = (smi_value * lambda_factor_value / value)
                            number += 1                        
                        else:
                            Ci_table[i, j] = 0
                        counter +=1
                        Ci_table_sum += Ci_table[i, j]
                        lambda_factor_sum += lambda_factor_value
                        
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
                                
                    
                    utils.output_to_file(Ci_table_no_heatpoints,Path.joinpath(temporary_folder,f"{prename}{element}_Ci_no_heatpoints"))               
                    utils.Ci_saving_dat(Ci_table, output_path, element, 1000)
                    utils.Ci_saving_plot(Ci_table, output_path, element, pixel_size, color_of_heatmap, 1000, ".png")
                    utils.output_to_file(lambda_factor, Path.joinpath(output_path, f"{prename}{element}_lambda"))
                    with open(Path.joinpath(output_path, f"lambda_Ci_average.txt"), "a") as f:
                        f.write(f'element:  {element},  average lambda: {format(lambda_average_factor, ".2e")},    average Ci [g/g]: {format(Ci_average_factor, ".2e")}, \n')                        
                    
                    utils.output_to_file(Ci_table,Path.joinpath(temporary_folder,f"{prename}{element}_Ci"))            
                else:
                    print(f"No data for element: {element}. Skipping...")
                    continue

                

    print("Processing complete. Check the output folder for results.")

if __name__ == "__main__":
    main()
    
    
    
    
############ 
# Polyx - bez zeropeak i bez TXT (tylko CSV)  nazwy plików = prename_element-numerinii.csv --- Poli
# Tornado - TXT i zeropeak do obliczenia livetime. Nazwy plików = prename_element.txt --- Mono

# Format kolumny: X (współrzędna), Y=1, Z (współrzędna), stężenie pierwiastka 1, stężenie pierwiastka 2, stężenie pierwiastka 3, ... 

# Poprawić sensitivity na pierwiastek-numerlinii. 
# Dodać inne linie (ka, kb, La, Lb, M)


###--------------------------------------- DEADLINES.

###----------------------------------------- STYCZEŃ.

# Program działa na duzych mapach --------------------------------------- DONE

###----------------------------------------- LUTY.

# Dane z synchrotronu (nie ma lifetime - jeśli nie ma pliku to nie dzielimy) --------------------------------------- DONE
# Pisanie pracy + szlifowanie kodu 
# Point mode 
# Snip mode 
# WSTĘP TEORETYCZNY - coś ma być napisane. Coś o solaris, coś o energiach, że jedno mono drugie poli i wgl lanie wody. 
# jakiś szkielet - o czym wgl będziemy pisać. --------------------------------------- DONE

###----------------------------------------- MARZEC.

# Kod w formie .exe

###----------------------------------------- KWIECIEŃ.



    