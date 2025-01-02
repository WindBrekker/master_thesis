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

def quantify():
    print("Quantifying")
    
def colorbox(window):
    window.color_of_heatmap = str(window.colorbar_combobox.currentText())
    print(window.color_of_heatmap)  
    


def main(window, start_window_instance, title, main_folder_path, pixel_size_value, inputfile_name, zeropeak_name, scatter_name, sample_matrix_name, treshhold_value, spectrum):
    window.show()
    path = Path(main_folder_path)
    if not path.exists():
        start_window_instance.input_info_label.setText("The specified folder does not exist.")
        start_window_instance.input_info_label.setStyleSheet("color: red")
        # window.close()
    else:
        pass

    window.use_for_mask_button.setEnabled(True)
    window.use_for_mask_button.clicked.connect(quantify)
    window.colorbar_combobox.activated.connect(colorbox)
    


    


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = new_window.NewWindow("Title")
    sys.exit(app.exec())