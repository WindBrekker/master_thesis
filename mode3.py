import sys
import shutil
import os
import utils
import numpy as np
from pathlib import Path
from os.path import exists as file_exists
from PyQt6.QtGui import QPalette, QColor, QIcon, QAction, QPixmap
from PyQt6.QtWidgets import QApplication
import start_window
import new_window

def main(window, title, main_folder_path, pixel_size_value, inputfile_name, zeropeak_name, scatter_name, sample_matrix_name, treshhold_value):
    window.show()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = new_window.NewWindow()
    sys.exit(app.exec())