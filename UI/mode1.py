import sys
import shutil
import os
import utils
import numpy as np
from pathlib import Path
from os.path import exists as file_exists
from PyQt6.QtGui import QPalette, QColor, QIcon, QAction, QPixmap
from PyQt6.QtWidgets import QApplication
import new_window
import quantify
import plotly.express as px



def main(window, start_window_instance, title, main_folder_path, pixel_size_value, 
         inputfile_name, zeropeak_name, scatter_name, 
         sample_matrix_name, treshhold_value, spectrum, zeropeak_coefficients_name,
         scatter_coefficients_name):
    
    window.show()
    main_folder_path = Path(main_folder_path)
    if not main_folder_path.exists():
        start_window_instance.input_info_label.setText(
            "The specified folder does not exist.")
        start_window_instance.input_info_label.setStyleSheet("color: red")
        window.close()
    else:
        if not file_exists(os.path.join(main_folder_path, inputfile_name)):
            start_window_instance.input_info_label.setText(
                "There is no input file in the specified folder.")
            start_window_instance.input_info_label.setStyleSheet("color: red")
            print(os.path.join(main_folder_path, inputfile_name))
            window.close()
        elif not file_exists(os.path.join(main_folder_path, zeropeak_coefficients_name)) and spectrum == "Poli":
            start_window_instance.input_info_label.setText(
                "There is no zero peak file in the specified folder.")
            start_window_instance.input_info_label.setStyleSheet("color: red")
            print(os.path.join(main_folder_path, zeropeak_coefficients_name))
            window.close()
        elif not file_exists(os.path.join(main_folder_path, scatter_coefficients_name)):
            start_window_instance.input_info_label.setText(
                "There is no scatter file in the specified folder.")
            start_window_instance.input_info_label.setStyleSheet("color: red")
            print(os.path.join(main_folder_path, scatter_coefficients_name))
            window.close()
        elif not file_exists(os.path.join(main_folder_path, sample_matrix_name)):
            start_window_instance.input_info_label.setText(
                "There is no sample matrix file in the specified folder.")
            start_window_instance.input_info_label.setStyleSheet("color: red")
            print(os.path.join(main_folder_path, sample_matrix_name))
            window.close()
        else:
            start_window_instance.input_info_label.setStyleSheet(
                "color: transparent")
            if os.listdir(main_folder_path):
                main_folder_insides = os.listdir(main_folder_path)
                window.folders_names = [file for file in main_folder_insides if os.path.isdir(Path.joinpath(main_folder_path, file)) and not file.endswith("_output")]
                window.prefere_folder_combobox.addItems(window.folders_names)
            else:
                window.prefere_folder_combobox.setPlaceholderText(
                    "No subfolders detected")

    window.quantify_button.setDisabled(True)
    utils.load_input_files(main_folder_path, inputfile_name, window)
    utils.load_scatter_file(main_folder_path, scatter_coefficients_name, window)
    utils.load_sample_matrix_file(main_folder_path, sample_matrix_name, window)
    print(spectrum)
    if spectrum == "Poli":
        utils.load_zeropeak_file(main_folder_path, zeropeak_coefficients_name, window)
    elif spectrum == "Mono":
        pass
    window.previous_element_button.setDisabled(True)
    window.next_element_button.setDisabled(True)
    window.use_for_mask_button.clicked.connect(lambda: utils.use_for_mask(window))
    window.colorbar_combobox.activated.connect(lambda: utils.colorbox(window))
    window.prefere_folder_combobox.activated.connect(lambda: utils.box_folder_changed(window, zeropeak_name, scatter_name, spectrum, main_folder_path, treshhold_value))
    window.quantify_button.clicked.connect(lambda: quantify.quantify(window, main_folder_path, pixel_size_value, inputfile_name, zeropeak_name, scatter_name, sample_matrix_name, treshhold_value, spectrum, zeropeak_coefficients_name, scatter_coefficients_name))
    window.confirm_saving_button.clicked.connect(lambda: utils.save_quantification_data(window))
    window.exiting_button.clicked.connect(lambda: exit_program)

def exit_program():
    sys.exit(app.exec())
if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = new_window.NewWindow("QuantSlice")
    sys.exit(app.exec())
