import sys
import shutil
import os
import numpy as np
from pathlib import Path
from os.path import exists as file_exists
from PyQt6.QtGui import QPalette, QColor, QIcon, QAction, QPixmap
import start_window
import new_window
import xraylib as xr
import math
import matplotlib.pyplot as plt

# def refresh():
#     pass

# def folder_changed(folder_combobox_text):
#     current_folder_name = folder_combobox_text
#     print(current_folder_name)

def file_to_list(input):
    try:
        converted_array = np.loadtxt(input, delimiter=',')
        return converted_array
    except:
        print("Couldn't find data")
        print(input)
        return None

def use_for_mask(current_element, mask_label):
    element = current_element.text()
    mask_label.set_text(element)



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

def antimask_creating(element, path, folder, prename, treshold, color, separator):
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




def Quantify(input_folder_path):
    folder_path = input_folder_path
    _initialize_folder_variables(folder_path)
    _calculate_livetime_with_zeropeak()
    _create_output_folders()
    _process_scatter_data()
    _calculate_sample_mass()
    _process_elements()
    _finalize_quantification()

def _initialize_folder_variables(folder_path):
    file_names = os.listdir(Path(folder_path))
    first_file = file_names[0]
    splitted_file = first_file.rsplit("_", 1)
    prename = splitted_file[0]
    separator = "_"

def _calculate_livetime_with_zeropeak(self):
    zeropeak_matrix = utils.file_to_list(Path(os.path.join(self.Main_Folder_Path, self.folder, f"{self.prename}{self.separator}{self.zeropeak_name}.txt")))
    self.livetime_matrix = utils.LT_calc(zeropeak_matrix, self.zeropeak_dict["a"], self.zeropeak_dict["b"])
    utils.output_to_file(self.livetime_matrix, Path(os.path.join(self.Main_Folder_Path, f"{self.folder}_output", f"{self.prename}_livetime_map")))
    self.mask_map = utils.mask_creating(self.elements_in_nodec[0], self.Main_Folder_Path, self.folder, self.prename, self.treshold, self.color_of_heatmap, self.separator)
    self.antimask_map = utils.antimask_creating(self.elements_in_nodec[0], self.Main_Folder_Path, self.folder, self.prename, self.treshold, self.color_of_heatmap, self.separator)

def _create_output_folders(self):
    if not Path(os.path.join(self.Main_Folder_Path, "temporary")).exists():
        Path(os.path.join(self.Main_Folder_Path, "temporary")).mkdir()
    if not Path(os.path.join(self.Main_Folder_Path, f"{self.folder}_output")).exists():
        Path(os.path.join(self.Main_Folder_Path, f"{self.folder}_output")).mkdir()
    if not Path(os.path.join(self.Main_Folder_Path, "temporary", f"{self.folder}_output")).exists():
        Path(os.path.join(self.Main_Folder_Path, "temporary", f"{self.folder}_output")).mkdir()
    self.temporary_folder = Path(os.path.join(self.Main_Folder_Path, "temporary", f"{self.folder}_output"))

def _process_scatter_data(self):
    scater_tab = utils.file_to_list(os.path.join(self.Main_Folder_Path, self.folder, f"{self.prename}{self.separator}{self.scater_name}.txt"))
    for i in range(len(scater_tab)):
        for j in range(len(scater_tab[0])):
            scater_tab[i][j] = scater_tab[i][j] / float(self.livetime_matrix[i][j])
    self._create_antimask_scatter(scater_tab)

def _create_antimask_scatter(self, scater_tab):
    antimask_scater = [[scater_tab[i][j] * self.antimask_map[i][j] for j in range(len(scater_tab[0]))] for i in range(len(scater_tab))]
    scater_treshold = np.min(scater_tab)
    antimask_scater_mask = [[1 if self.antimask_map[i][j] and antimask_scater[i][j] < (1.25 * scater_treshold) else 0 for j in range(len(scater_tab[0]))] for i in range(len(scater_tab))]
    utils.output_to_file(antimask_scater_mask, os.path.join(self.temporary_folder, "antimask_scater_mask"))
    self._calculate_antimask_mean(antimask_scater, antimask_scater_mask)

def _calculate_antimask_mean(self, antimask_scater, antimask_scater_mask):
    antimask_sum = sum(antimask_scater[i][j] for i in range(len(antimask_scater)) for j in range(len(antimask_scater[0])) if antimask_scater_mask[i][j])
    iteration_antimask = sum(1 for i in range(len(antimask_scater)) for j in range(len(antimask_scater[0])) if antimask_scater_mask[i][j])
    antimask_mean = antimask_sum / iteration_antimask
    self._create_sample_mass_livetime(antimask_mean)

def _create_sample_mass_livetime(self, antimask_mean):
    scater_tab = utils.file_to_list(os.path.join(self.Main_Folder_Path, self.folder, f"{self.prename}{self.separator}{self.scater_name}.txt"))
    sm_livetime = [[max(scater_tab[i][j] - antimask_mean, 0) for j in range(len(scater_tab[0]))] for i in range(len(scater_tab))]
    sm = utils.SampSM_calc(sm_livetime, self.scater_dict["a"], self.scater_dict["b"])
    sm_masked = [[sm[i][j] * self.mask_map[i][j] for j in range(len(sm[0]))] for i in range(len(sm))]
    utils.output_to_file(sm_masked, os.path.join(self.temporary_folder, "sample_mass_noc"))

def _process_elements(self):
    for key in self.Z_number_per_element_dict:
        element = key
        if file_exists(os.path.join(self.Main_Folder_Path, self.folder, f"{self.prename}{self.separator}{element}.txt")):
            self._process_element_data(element)

def _process_element_data(self, element):
    K_i = float(self.K_value_per_element_dict[element])
    counts_data = os.path.join(self.Main_Folder_Path, self.folder, f"{self.prename}{self.separator}{element}.txt")
    counts_table = utils.file_to_list(counts_data)
    table_of_smi = [[(counts_table[i][j] * self.mask_map[i][j]) / self.livetime_matrix[i][j] / K_i for j in range(len(counts_table[0]))] for i in range(len(counts_table))]
    utils.output_to_file(table_of_smi, os.path.join(self.temporary_folder, f"{element}_element_mass_noc"))
    self._calculate_Ci_table(element, table_of_smi)

def _calculate_Ci_table(self, element, table_of_smi):
    sm = utils.file_to_list(os.path.join(self.temporary_folder, "sample_mass_noc"))
    Ci_table = [[0 for _ in range(len(sm[0]))] for _ in range(len(sm))]
    lambda_factor = [[0 for _ in range(len(sm[0]))] for _ in range(len(sm))]
    counter, Ci_table_sum, lambda_factor_sum = 0, 0, 0
    for i in range(len(sm)):
        for j in range(len(sm[0])):
            if table_of_smi[i][j] != 0:
                lambda_factor[i][j] = utils.lambda_factor(sm[i][j], int(self.Z_number_per_element_dict[element]), float(self.energy_per_element_dict[element]), self.concentration_per_element_dict)
                if sm[i][j] > 0.3 * np.median(sm) and table_of_smi[i][j] >= 0:
                    Ci_table[i][j] = (table_of_smi[i][j] * lambda_factor[i][j] / sm[i][j])
                counter += 1
                Ci_table_sum += Ci_table[i][j]
                lambda_factor_sum += lambda_factor[i][j]
    lambda_average_factor = lambda_factor_sum / counter
    Ci_average_factor = Ci_table_sum / counter
    self._finalize_Ci_table(element, Ci_table, lambda_factor, lambda_average_factor, Ci_average_factor)

def _finalize_Ci_table(self, element, Ci_table, lambda_factor, lambda_average_factor, Ci_average_factor):
    Ci_table_no_heatpoints = [[0 if Ci_table[i][j] > 10 * Ci_average_factor else Ci_table[i][j] for j in range(len(Ci_table[0]))] for i in range(len(Ci_table))]
    utils.output_to_file(Ci_table_no_heatpoints, os.path.join(self.Main_Folder_Path, "temporary", f"{self.folder}_output", f"{self.prename}_{element}_Ci_no_heatpoints"))
    utils.output_to_file(lambda_factor, os.path.join(self.Main_Folder_Path, f"{self.folder}_output", f"{self.prename}_{element}_lambda"))
    with open(os.path.join(self.Main_Folder_Path, f"{self.folder}_output", "lambda_Ci_average.txt"), "a") as f:
        f.write(f'element:  {element},  average lambda: {format(lambda_average_factor, ".2e")},    average Ci [g/g]: {format(Ci_average_factor, ".2e")}, \n')
    utils.output_to_file(Ci_table, os.path.join(self.Main_Folder_Path, "temporary", f"{self.folder}_output", f"{self.prename}_{element}_Ci"))

def _finalize_quantification(self):
    self.chosen_folder = self.Prefere_folder.currentText()
    self.confirm_names_button.disconnect()
    self.confirm_names_button.setEnabled(False)
    self.previous_element_button.disconnect()
    self.previous_element_button.clicked.connect(self.previous_element_final)
    self.next_element_button.disconnect()
    self.next_element_button.clicked.connect(self.next_element_final)
    self.quantify_button.disconnect()
    self.quantify_button.setText("Go back")
    self.quantify_button.clicked.connect(self.Back_to_quantify)
    self.Prefere_folder.activated.disconnect()
    self.Prefere_folder.activated.connect(self.new_prefered_folder)
    iteration = 0
    while not Path(os.path.join(self.Main_Folder_Path, "temporary", f"{self.chosen_folder}_output", f"{self.prename}_{self.elements_in_nodec[iteration]}_Ci.txt")).exists():
        iteration += 1
    self._save_final_plots(iteration)

def _save_final_plots(self, iteration):
    plt.imshow(utils.file_to_list(os.path.join(self.Main_Folder_Path, "temporary", f"{self.chosen_folder}_output", f"{self.prename}_{self.elements_in_nodec[iteration]}_Ci.txt")), cmap=self.color_of_heatmap, interpolation="nearest")
    plt.title("Concentration map")
    plt.colorbar()
    plt.savefig(os.path.join(self.Main_Folder_Path, "temporary", f"{self.chosen_folder}_output", f"{self.prename}_{self.elements_in_nodec[iteration]}_Ci.png"))
    plt.close()
    plt.imshow(utils.file_to_list(os.path.join(self.Main_Folder_Path, "temporary", f"{self.chosen_folder}_output", f"{self.prename}_{self.elements_in_nodec[iteration]}_Ci_no_heatpoints.txt")), cmap=self.color_of_heatmap, interpolation="nearest")
    plt.title("Concentration map without heatpoints")
    plt.colorbar()
    plt.savefig(os.path.join(self.Main_Folder_Path, "temporary", f"{self.chosen_folder}_output", f"{self.prename}_{self.elements_in_nodec[iteration]}_Ci_no_heatpoints.png"))
    plt.close()
    self.sample_pixmap = QPixmap(os.path.join(self.Main_Folder_Path, "temporary", f"{self.chosen_folder}_output", f"{self.prename}_{self.elements_in_nodec[iteration]}_Ci.png"))
    self.sample_picture_label.setPixmap(self.sample_pixmap)
    self.sample_pixmap2 = QPixmap(os.path.join(self.Main_Folder_Path, "temporary", f"{self.chosen_folder}_output", f"{self.prename}_{self.elements_in_nodec[iteration]}_Ci_no_heatpoints.png"))
    self.sample_picture_label2.setPixmap(self.sample_pixmap2)
    element_table_not_masked = np.array(utils.file_to_list(os.path.join(self.Main_Folder_Path, "temporary", f"{self.chosen_folder}_output", f"{self.elements_in_nodec[iteration]}_element_mass_noc.txt")))
    self.element_table = element_table_not_masked[element_table_not_masked != 0]
    self.Mean_value_label.setText(str(np.average(self.element_table)))
    self.Median_value_label.setText(str(np.median(self.element_table)))
    self.Min_value_label.setText(str(np.min(self.element_table)))
    self.Max_value_label.setText(str(np.max(self.element_table)))
    self.saving_button.setEnabled(True)    
