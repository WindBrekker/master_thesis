import sys
from PyQt6.QtWidgets import QApplication, QMainWindow, QPushButton, QVBoxLayout, QWidget, QLabel, QLineEdit
import backend.utils as utils
import mode1
import mode2
import mode3
import start_window
import new_window

def main():
    app = QApplication(sys.argv)
    main_window = start_window.StartWindow()
    main_window.show()
    sys.exit(app.exec())

if __name__ == "__main__":
    main()
    
    
