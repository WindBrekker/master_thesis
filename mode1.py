import sys
import shutil
import os
import utils
import numpy as np
from pathlib import Path
from os.path import exists as file_exists
from PyQt6.QtGui import QPalette, QColor, QIcon, QAction, QPixmap
from pathlib import Path
from PyQt6.QtWidgets import QApplication
import start_window
import new_window
    
def main(title, main_folder_path, pixel_size_value, inputfile_name, zeropeak_name, scatter_name, sample_matrix_name, treshhold_value):
    app = QApplication(sys.argv)
    app.main_window = new_window.NewWindow()
    app.main_window.show()

    
    print(main_folder_path)
    app.exec()
    

##some code



if __name__ == "__main__":
    main()
