import sys
from PyQt6.QtWidgets import QApplication, QMainWindow, QPushButton, QVBoxLayout, QWidget, QLabel, QLineEdit
import utils
import mode3
import mode2
import mode1

class StartWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        
        self.mode1 = "Point"
        self.mode2 = "Snip"
        self.mode3 = "Full map"
        
        self.setWindowTitle("SliceQuant")
        
        # Create buttons
        self.button1 = QPushButton(self.mode1)
        self.button2 = QPushButton(self.mode2)
        self.button3 = QPushButton(self.mode3)
        self.next_button = QPushButton("Next")
        
        # Connect buttons to the methods
        self.button1.clicked.connect(self.open_window1)
        self.button2.clicked.connect(self.open_window2)
        self.button3.clicked.connect(self.open_window3)
        self.next_button.clicked.connect(self.open_next_window)
        
        # Create label
        self.start_window_label = QLabel("Choose the work mode")
        self.input_info_label = QLabel("Enter the appropriate values and (optional) used nomenclature",self)
        
        # Create edit lines
        self.Main_folder = QLineEdit(self)
        self.Main_folder.setPlaceholderText("Main folder path")
        self.Pixel = QLineEdit(self)
        self.Pixel.setPlaceholderText("1000")
        self.Inputfile = QLineEdit(self)
        self.Inputfile.setPlaceholderText("inputfile")
        self.Zeropeak = QLineEdit(self)
        self.Zeropeak.setPlaceholderText("zeropeak")
        self.Scater = QLineEdit(self)    
        self.Scater.setPlaceholderText("scater")
        self.SampMatrix = QLineEdit(self)
        self.SampMatrix.setPlaceholderText("sample_matrix")
        self.Treshold = QLineEdit(self)
        self.Treshold.setPlaceholderText("10")
        
        # Layouts
        layout = QVBoxLayout()
        layout.addWidget(self.start_window_label)
        layout.addWidget(self.button1)
        layout.addWidget(self.button2)
        layout.addWidget(self.button3)
        layout.addWidget(self.input_info_label)
        layout.addWidget(self.Main_folder)
        layout.addWidget(self.Pixel)
        layout.addWidget(self.Inputfile)
        layout.addWidget(self.Zeropeak)
        layout.addWidget(self.Scater)
        layout.addWidget(self.SampMatrix)
        layout.addWidget(self.Treshold)
        layout.addWidget(self.next_button)
        
        # Set the layout to a QWidget
        container = QWidget()
        container.setLayout(layout)
        
        # Set the central widget
        self.setCentralWidget(container)
    
    def open_window1(self):
        self.mode_number = 1

    def open_window2(self):
        self.mode_number = 2

    def open_window3(self):
        self.mode_number = 3
        
    def open_next_window(self):
        self.main_folder_path = str(self.Main_folder.text())
        self.pixel_size_value = str(self.Pixel.text())
        self.inputfile_name = str(self.Inputfile.text())
        self.zeropeak_name = str(self.Zeropeak.text())
        self.scatter_name = str(self.Scater.text())
        self.sample_matrix_name = str(self.SampMatrix.text())
        self.treshhold_value = str(self.Treshold.text())
        
        if self.pixel_size_value == "":
            self.pixel_size_value = 1000
        if self.inputfile_name == "":
            self.inputfile_name = "inputfile"
        if self.zeropeak_name == "":
            self.zeropeak_name = "zeropeak"
        if self.scatter_name == "":
            self.scatter_name = "scater"
        if self.sample_matrix_name== "":
            self.sample_matrix_name = "sample_matrix"
        if self.treshhold_value == "":
            self.treshhold_value = 10
        
        
        print(self.pixel_size_value)
        print(self.inputfile_name)
        print(self.scatter_name)
        print(self.sample_matrix_name)
        print(self.treshhold_value)
        print(self.main_folder_path)
        
        
        if not (self.main_folder_path == ""):
            if (self.mode_number == 1):
                mode1.main(self.mode1, self.main_folder_path, self.pixel_size_value, self.inputfile_name, self.zeropeak_name, self.scatter_name, self.sample_matrix_name, self.treshhold_value)
            elif (self.mode_number == 2):
                mode2.main(self.mode2, self.main_folder_path, self.pixel_size_value, self.inputfile_name, self.zeropeak_name, self.scatter_name, self.sample_matrix_name, self.treshhold_value)
            elif (self.mode_number == 3):
                mode3.main(self.mode3, self.main_folder_path, self.pixel_size_value, self.inputfile_name, self.zeropeak_name, self.scatter_name, self.sample_matrix_name, self.treshhold_value)
        else:
            print("There's an empty value in Main Folder Path line. Fix it before next attepmt")