# start_window.py
import sys
from PyQt6.QtWidgets import QApplication, QMainWindow, QPushButton, QVBoxLayout, QWidget, QLabel, QLineEdit, QCheckBox, QHBoxLayout,QMessageBox
import utils
import mode3
import mode2
import mode1
import new_window


class ToggleSwitch(QCheckBox):
    def __init__(self):
        super().__init__()
        self.setFixedSize(30, 15)
        self.setStyleSheet("""
            QCheckBox {
                background-color: #ccc;
                border-radius: 15px;
                width: 30px;
                height: 15px;
                padding: 0px;
            }
            QCheckBox::indicator {
                width: 15px;
                height: 15px;
                border-radius: 15px;
            }
            QCheckBox::indicator:checked {
                background-color: #3498db; /* Blue */
                margin-left: 15px;
            }
            QCheckBox::indicator:unchecked {
                background-color: #e74c3c; /* Red */
                margin-left: 0px;
            }
        """)
        self.setChecked(False)  # Start in the "Red" state

class StartWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        
        self.mode1 = "Full map mode"
        self.mode2 = "Snip mode"
        self.mode3 = "Point mode"
        self.spectrum = "Poli"
        
        self.setWindowTitle("SliceQuant")
        
        # Create buttons
        self.button1 = QPushButton(self.mode1)
        readme_button = QPushButton("README / Help")
        
        self.button1.setCheckable(True)
        self.button2 = QPushButton(self.mode2)
        self.button2.setCheckable(True)
        # self.button3 = QPushButton(self.mode3)
        # self.button3.setCheckable(True)
        self.next_button = QPushButton("Next")
        self.next_button.setDisabled(True)
        
        # Connect buttons to the methods
        self.button1.clicked.connect(self.open_window1)
        self.button2.clicked.connect(self.open_window2)
        # self.button3.clicked.connect(self.open_window3)
        self.next_button.clicked.connect(self.open_next_window)
        readme_button.clicked.connect(self.show_readme)
        
        
        # Create label
        self.start_window_label = QLabel("Choose the work mode")
        self.input_info_label = QLabel("Enter the appropriate values and (optional) used nomenclature", self)
        self.checkbox_label = QLabel("Choose spectrum mode", self)
        self.poli_spectrum_label = QLabel("Polichromatic spectrum")
        self.mono_spectrum_label = QLabel("Monochromatic spectrum")
        
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
        self.Scater_Coefficients = QLineEdit(self)
        self.Scater_Coefficients.setPlaceholderText("scater_coefficients")
        self.Zeropeak_Coefficients = QLineEdit(self)
        self.Zeropeak_Coefficients.setPlaceholderText("zeropeak_coefficients")
        
        
        # Checkboxes
        self.checkbox1 = ToggleSwitch()
        self.checkbox1.toggled.connect(lambda: self.set_spectrum_mode())
        
        # Layouts
        sublayout = QHBoxLayout()
        sublayout.addWidget(self.poli_spectrum_label)
        sublayout.addStretch(1)
        sublayout.addWidget(self.checkbox1)
        sublayout.addStretch(1) 
        sublayout.addWidget(self.mono_spectrum_label)
        layout = QVBoxLayout()
        layout.addWidget(self.start_window_label)
        layout.addWidget(self.button1)
        layout.addWidget(self.button2)
        # layout.addWidget(self.button3)
        layout.addWidget(self.checkbox_label)
        layout.addLayout(sublayout)
        layout.addWidget(self.input_info_label)
        layout.addWidget(self.Main_folder)
        layout.addWidget(self.Pixel)
        layout.addWidget(self.Inputfile)
        layout.addWidget(self.Zeropeak)
        layout.addWidget(self.Scater)
        layout.addWidget(self.Scater_Coefficients)
        layout.addWidget(self.Zeropeak_Coefficients)
        layout.addWidget(self.SampMatrix)
        layout.addWidget(self.Treshold)
        layout.addWidget(self.next_button)
        layout.addWidget(readme_button)
        
        

        
        # Set the layout to a QWidget
        container = QWidget()
        container.setLayout(layout)
        
        # Set the central widget
        self.setCentralWidget(container)

        
    
    def set_spectrum_mode(self):
        if self.checkbox1.isChecked():
            self.spectrum = "Mono"
            self.Zeropeak.setDisabled(True)   
            self.Zeropeak_Coefficients.setDisabled(True)
        else: 
            self.spectrum = "Poli"
            self.Zeropeak.setDisabled(False)
            self.Zeropeak_Coefficients.setDisabled(False)
        
    
    def open_window1(self):
        self.mode_number = 1
        self.button1.setChecked(True)
        self.button2.setChecked(False)
        # self.button3.setChecked(False)
        self.next_button.setDisabled(False)

    def open_window2(self):
        self.mode_number = 2
        self.button1.setChecked(False)
        self.button2.setChecked(True)
        # self.button3.setChecked(False)
        self.next_button.setDisabled(False)

        


    def open_window3(self):
        self.mode_number = 3
        self.button1.setChecked(False)
        self.button2.setChecked(False)
        # self.button3.setChecked(True)
        self.next_button.setDisabled(False)
        
    def show_readme(self):
        instructions = (
            "Welcome to the App!\n\n"
            "Instructions:\n"
            "1. Choose the work mode by clicking on the buttons.\n"
            "2. Enter the appropriate values in the input fields.\n"
            "3. If you are using the Polichromatic spectrum, enter the zero peak and scatter coefficients.\n"
            "4. If you are using the Monochromatic spectrum, leave the zero peak and scatter coefficients fields empty.\n"
            "5. Data shall be organised as follows:\n"
            "   - Main folder containing all datasets in separated subfolders, inputfile, sample_matrix, scatter and/or zeropeak coefficients\n"
            "   - - Subfolders with element-separated data matrix, scatter matrix and/or zeropeak matrix .\n"
        )
        QMessageBox.information(self, "How to Use", instructions)


        
    def open_next_window(self):
        self.main_folder_path = str(self.Main_folder.text())
        self.pixel_size_value = str(self.Pixel.text())
        self.inputfile_name = str(self.Inputfile.text())
        self.zeropeak_name = str(self.Zeropeak.text())
        self.scatter_name = str(self.Scater.text())
        self.zeropeak_coefficients_name = str(self.Zeropeak_Coefficients.text())
        self.scatter_coefficients_name = str(self.Scater_Coefficients.text())
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
        if self.zeropeak_coefficients_name == "":
            self.zeropeak_coefficients_name = "zeropeak_coefficients"
        if self.scatter_coefficients_name == "":
            self.scatter_coefficients_name = "scater_coefficients"
        if self.sample_matrix_name == "":
            self.sample_matrix_name = "sample_matrix"
        if self.treshhold_value == "":
            self.treshhold_value = 10
        
        if not (self.main_folder_path == ""):
            if self.mode_number == 1:
                self.new_window = new_window.NewWindow(self.mode1)
                mode1.main(self.new_window, self, self.mode1, self.main_folder_path, self.pixel_size_value, self.inputfile_name, self.zeropeak_name, self.scatter_name, self.sample_matrix_name, self.treshhold_value, self.spectrum, self.zeropeak_coefficients_name, self.scatter_coefficients_name)
            elif self.mode_number == 2:
                self.new_window = new_window.NewWindow(self.mode2)
                self.new_window.show()
                mode2.main(self.new_window, self, self.mode2, self.main_folder_path, self.pixel_size_value, self.inputfile_name, self.zeropeak_name, self.scatter_name, self.sample_matrix_name, self.treshhold_value, self.spectrum, self.zeropeak_coefficients_name, self.scatter_coefficients_name)
            elif self.mode_number == 3:
                self.new_window = new_window.NewWindow(self.mode3)
                self.new_window.show()
                mode3.main(self.new_window, self, self.mode3, self.main_folder_path, self.pixel_size_value, self.inputfile_name, self.zeropeak_name, self.scatter_name, self.sample_matrix_name, self.treshhold_value, self.spectrum, self.zeropeak_coefficients_name, self.scatter_coefficients_name)
        else:
            print("There's an empty value in Main Folder Path line. Fix it before next attempt")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    main_window = StartWindow()
    main_window.show()
    sys.exit(app.exec())