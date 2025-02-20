import sys
import shutil
import os
import backend.utils as utils
import numpy as np
from pathlib import Path
from os.path import exists as file_exists
from PyQt6.QtGui import QPalette, QColor, QIcon, QAction, QPixmap
from PyQt6.QtWidgets import QApplication
import new_window

def quantify():
    print("Quantifying")
    
def colorbox(window):
    window.color_of_heatmap = str(window.colorbar_combobox.currentText())
    


def main(window, start_window_instance, title, main_folder_path, pixel_size_value, inputfile_name, zeropeak_name, scatter_name, sample_matrix_name, treshhold_value, spectrum):
    window.show()
    path = Path(main_folder_path)
    if not path.exists():
        start_window_instance.input_info_label.setText("The specified folder does not exist.")
        start_window_instance.input_info_label.setStyleSheet("color: red")
        window.close()
    else:
        if not file_exists(os.path.join(path, inputfile_name)):
            start_window_instance.input_info_label.setText("There is no input file in the specified folder.")
            start_window_instance.input_info_label.setStyleSheet("color: red")
            print(os.path.join(path, inputfile_name))
            window.close()
        elif not file_exists(os.path.join(path, zeropeak_name)) and spectrum == "Poli":
            start_window_instance.input_info_label.setText("There is no zero peak file in the specified folder.")
            start_window_instance.input_info_label.setStyleSheet("color: red")
            print(os.path.join(path, zeropeak_name))
            window.close()
        elif not file_exists(os.path.join(path, scatter_name)):
            start_window_instance.input_info_label.setText("There is no scatter file in the specified folder.")
            start_window_instance.input_info_label.setStyleSheet("color: red")
            print(os.path.join(path, scatter_name))
            window.close()
        elif not file_exists(os.path.join(path, sample_matrix_name)):
            start_window_instance.input_info_label.setText("There is no sample matrix file in the specified folder.")
            start_window_instance.input_info_label.setStyleSheet("color: red")
            print(os.path.join(path, sample_matrix_name))
            window.close()
        else:
            start_window_instance.input_info_label.setStyleSheet("color: transparent")
            if os.listdir(path):
                window.folders_names = [file for file in os.listdir(path) if os.path.isdir(os.path.join(path,file))]
                window.prefere_folder_combobox.addItems(window.folders_names)
            else:
                window.prefere_folder_combobox.setPlaceholderText("No subfolders detected")

    window.use_for_mask_button.clicked.connect(quantify)
    window.colorbar_combobox.activated.connect(lambda: colorbox(window))
    window.prefere_folder_combobox.activated.connect(lambda: utils.folder_changed(window.prefere_folder_combobox.currentText()))
    


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = new_window.NewWindow("QuantSlice")
    sys.exit(app.exec())
    
    
    
    
    
    
    
    