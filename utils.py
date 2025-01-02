import sys
import shutil
import os
import numpy as np
from pathlib import Path
from os.path import exists as file_exists
from PyQt6.QtGui import QPalette, QColor, QIcon, QAction, QPixmap
import start_window
import new_window

def refresh():
    pass

def folder_changed():
    pass

def use_for_mask(current_element, mask_label):
    element = current_element.text()
    mask_label.set_text(element)