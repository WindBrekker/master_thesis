import sys
import shutil
import os
import utils
import numpy as np
from pathlib import Path
from os.path import exists as file_exists
from PyQt6.QtGui import QPalette, QColor, QIcon, QAction, QPixmap
from pathlib import Path
from PyQt6.QtWidgets import (
    QApplication,
    QLineEdit,
    QLabel,
    QMainWindow,
    QWidget,
    QVBoxLayout,
    QPushButton,
    QHBoxLayout,
    QComboBox,
    QCheckBox,
)
import mode3
import mode2     
import mode1


class Color(QWidget):

    def __init__(self, color):
        super(Color, self).__init__()
        self.setAutoFillBackground(True)

        palette = self.palette()
        palette.setColor(QPalette.ColorRole.Window, QColor(color))
        self.setPalette(palette)

class NewWindow(QMainWindow):
    def __init__(self, title):
        super().__init__()
        self.setWindowTitle(title)
        self.showMaximized
        
    #main layout
        pagelayout = QVBoxLayout()
    #sub layouts
        Upper_layout = QHBoxLayout()
        Lower_layout = QHBoxLayout()

    #sub upper_layouts
        Results_layout = QHBoxLayout()
    #sub lower_layout
        Left_layout = QVBoxLayout()
        Data_layout = QVBoxLayout()
    #data_layout
        Input_layout = QVBoxLayout()
        Names_layout = QVBoxLayout()
        Names_layout.addWidget(Color("transparent"))
        Saving_layout = QVBoxLayout()
        Saving_layout.addWidget(Color("transparent"))
    #sub saving_layout
        saving_button_layout = QHBoxLayout()
        saving_checkbox_Ci1_layout = QHBoxLayout()
        saving_checkbox_Ci2_layout = QHBoxLayout()
        saving_checkbox_SM1_layout = QHBoxLayout()
        saving_checkbox_SM2_layout = QHBoxLayout()
        saving_checkbox_SMi1_layout = QHBoxLayout()
        saving_checkbox_SMi2_layout = QHBoxLayout()
        saving_checkbox_Ci3_layout = QHBoxLayout()
        saving_checkbox_Ci4_layout = QHBoxLayout()
        saving_checkbox_SM3_layout = QHBoxLayout()
        saving_checkbox_SM4_layout = QHBoxLayout()
        saving_checkbox_SMi3_layout = QHBoxLayout()
        saving_checkbox_SMi4_layout = QHBoxLayout()
        
    #sub Left_layout
        Sample_layout = QHBoxLayout()
        Panel_layout = QHBoxLayout()
    #input_layout
        text_layout = QHBoxLayout()
        main_folder_layout = QHBoxLayout()
        pixel_size_layout = QHBoxLayout()            

        #Adding layouts
        pagelayout.addLayout(Upper_layout,1)
        pagelayout.addLayout(Lower_layout,9)

        Upper_layout.addLayout(Results_layout)

        Lower_layout.addLayout(Left_layout,6)
        Lower_layout.addWidget(Color("transparent"),1)
        Lower_layout.addLayout(Data_layout,3)

        Left_layout.addLayout(Panel_layout,2)
        Left_layout.addLayout(Sample_layout,8)

        Data_layout.addLayout(Input_layout,1)
        Data_layout.addLayout(Names_layout,3)
        Data_layout.addLayout(Saving_layout,5)
        Data_layout.addLayout(saving_button_layout,1)
        
        self.Ci_label = QLabel("Save the concentration maps as:",self)
        self.SM_label = QLabel("Save the sample mass per unit area map as:",self)
        self.SMi_label = QLabel("Save the element mass per unit area map as:",self)
        self.Ci_unit_label = QLabel("   With units:",self)
        self.SM_unit_label = QLabel("   With units:",self)
        self.SMi_unit_label = QLabel("  With units:",self)
        
        Saving_layout.addWidget(self.Ci_label)
        Saving_layout.addLayout(saving_checkbox_Ci1_layout)
        Saving_layout.addLayout(saving_checkbox_Ci2_layout)
        Saving_layout.addWidget(self.Ci_unit_label)
        Saving_layout.addLayout(saving_checkbox_Ci3_layout)
        Saving_layout.addLayout(saving_checkbox_Ci4_layout)
        Saving_layout.addWidget(self.SM_label)
        Saving_layout.addLayout(saving_checkbox_SM1_layout)
        Saving_layout.addLayout(saving_checkbox_SM2_layout)
        Saving_layout.addWidget(self.SM_unit_label)
        Saving_layout.addLayout(saving_checkbox_SM3_layout)
        Saving_layout.addLayout(saving_checkbox_SM4_layout)
        Saving_layout.addWidget(self.SMi_label)
        Saving_layout.addLayout(saving_checkbox_SMi1_layout)
        Saving_layout.addLayout(saving_checkbox_SMi2_layout)
        Saving_layout.addWidget(self.SMi_unit_label)
        Saving_layout.addLayout(saving_checkbox_SMi3_layout)
        Saving_layout.addLayout(saving_checkbox_SMi4_layout)
        
        Input_layout.addLayout(text_layout,2)
        Input_layout.addLayout(main_folder_layout,4)
        Input_layout.addLayout(pixel_size_layout,4)

        #Widgets
        #QLabel
        self.choose_main_folder_label = QLabel("Choose the main folder")
        self.colorbox_label = QLabel("Choose the heatmap colors")
        self.sample_picture_label = QLabel(self)
        self.sample_picture_label2 = QLabel(self)
        self.element_name_label = QLabel(self)
        self.element_name_label.setText("None")
        self.Cursor_data_label = QLabel("Cursor data",self)
        self.X_label = QLabel("X:",self)
        self.X_value_label = QLabel("",self)
        self.Y_label = QLabel("Y:",self)
        self.Y_value_label = QLabel("",self)
        self.Value_label = QLabel("Value:",self)
        self.Value_value_label = QLabel("",self)
        self.Mean_label = QLabel("Mean:",self)
        self.Mean_value_label = QLabel("",self)
        self.Median_label = QLabel("Median:",self)
        self.Median_value_label = QLabel("",self)
        self.Min_label = QLabel("Min:",self)
        self.Min_value_label = QLabel("",self)
        self.Max_label = QLabel("Max:",self)
        self.Max_value_label = QLabel("",self)
        self.Mask_label = QLabel("Mask:",self)
        self.Mask_value_label2 = QLabel("Current element:",self)
        self.Mask_value_label = QLabel("None",self)

        # #QComboBox
        self.colorbar_combobox = QComboBox(self)
        self.colorbar_combobox.addItems(["hot","viridis","plasma","inferno", "magma", "cividis", "coolwarm", "YlGnBu", "RdYlBu", "jet", "copper"])
        self.colorbar_combobox.setPlaceholderText("Choose colorbar")
        self.prefere_folder_combobox = QComboBox(self)
        self.prefere_folder_combobox.setPlaceholderText("Choose prefered folder")

        # #QCheckBox
        self.Ci_dat_checkbox = QCheckBox(".dat",self)
        self.Ci_png_checkbox = QCheckBox(".png",self)
        self.Ci_tiff_checkbox = QCheckBox(".tiff",self)
        self.Ci_bmp_checkbox = QCheckBox(".pdf",self)
        
        self.Ci_procent_checkbox = QCheckBox("%",self)
        self.Ci_mg_checkbox = QCheckBox("mg/g",self)
        self.Ci_ug_checkbox = QCheckBox("ug/g",self)
        self.Ci_auto_checkbox = QCheckBox("auto",self)
        
        self.sample_mass_dat_checkbox = QCheckBox(".dat",self)
        self.sample_mass_png_checkbox = QCheckBox(".png",self)
        self.sample_mass_tiff_checkbox = QCheckBox(".tiff",self)
        self.sample_mass_bmp_checkbox = QCheckBox(".pdf",self)
        
        self.sample_mass_g_checkbox = QCheckBox("g/g",self)
        self.sample_mass_mg_checkbox = QCheckBox("mg/g",self)
        self.sample_mass_ug_checkbox = QCheckBox("ug/g",self)
        self.sample_mass_ng_checkbox = QCheckBox("ng/g",self)      
            
        self.element_mass_dat_checkbox = QCheckBox(".dat",self)
        self.element_mass_png_checkbox = QCheckBox(".png",self)
        self.element_mass_tiff_checkbox = QCheckBox(".tiff",self)
        self.element_mass_bmp_checkbox = QCheckBox(".pdf",self)
        
        self.element_mass_g_checkbox = QCheckBox("g/g",self)
        self.element_mass_mg_checkbox = QCheckBox("mg/g",self)
        self.element_mass_ug_checkbox = QCheckBox("ug/g",self)
        self.element_mass_ng_checkbox = QCheckBox("ng/g",self) 
        
        # #QPixmap
        self.sample_pixmap = QPixmap('photo.png')
        self.sample_picture_label.setPixmap(self.sample_pixmap)
        self.sample_pixmap_2 = QPixmap('photo.png')
        

        # #QPushButton
        self.previous_element_button = QPushButton("<", self)
        self.next_element_button = QPushButton(">", self)
        self.use_for_mask_button = QPushButton("Use for mask", self)
        self.quantify_button = QPushButton("Quantify", self)
        

        self.confirm_saving_button = QPushButton("Confirm",self)
        
        self.saving_button = QPushButton("Save and Exit",self)
        self.saving_button.setEnabled(False)


        # #Adding widgets
        Names_layout.addWidget(self.colorbox_label)
        Names_layout.addWidget(self.colorbar_combobox)
        Names_layout.addWidget(self.prefere_folder_combobox)
        
        saving_checkbox_Ci1_layout.addWidget(self.Ci_dat_checkbox)
        saving_checkbox_Ci1_layout.addWidget(self.Ci_bmp_checkbox)
        saving_checkbox_Ci2_layout.addWidget(self.Ci_png_checkbox)
        saving_checkbox_Ci2_layout.addWidget(self.Ci_tiff_checkbox)

        saving_checkbox_Ci3_layout.addWidget(self.Ci_procent_checkbox)
        saving_checkbox_Ci3_layout.addWidget(self.Ci_mg_checkbox)
        saving_checkbox_Ci4_layout.addWidget(self.Ci_ug_checkbox)
        saving_checkbox_Ci4_layout.addWidget(self.Ci_auto_checkbox)    

        saving_checkbox_SM1_layout.addWidget(self.sample_mass_dat_checkbox)
        saving_checkbox_SM1_layout.addWidget(self.sample_mass_png_checkbox)
        saving_checkbox_SM2_layout.addWidget(self.sample_mass_tiff_checkbox)
        saving_checkbox_SM2_layout.addWidget(self.sample_mass_bmp_checkbox)

        saving_checkbox_SM3_layout.addWidget(self.sample_mass_g_checkbox)
        saving_checkbox_SM3_layout.addWidget(self.sample_mass_mg_checkbox)
        saving_checkbox_SM4_layout.addWidget(self.sample_mass_ug_checkbox)
        saving_checkbox_SM4_layout.addWidget(self.sample_mass_ng_checkbox)       

        saving_checkbox_SMi1_layout.addWidget(self.element_mass_dat_checkbox)
        saving_checkbox_SMi1_layout.addWidget(self.element_mass_png_checkbox)
        saving_checkbox_SMi2_layout.addWidget(self.element_mass_tiff_checkbox)
        saving_checkbox_SMi2_layout.addWidget(self.element_mass_bmp_checkbox)

        saving_checkbox_SMi3_layout.addWidget(self.element_mass_g_checkbox)
        saving_checkbox_SMi3_layout.addWidget(self.element_mass_mg_checkbox)
        saving_checkbox_SMi4_layout.addWidget(self.element_mass_ug_checkbox)
        saving_checkbox_SMi4_layout.addWidget(self.element_mass_ng_checkbox)
        
        saving_button_layout.addWidget(self.confirm_saving_button)
        saving_button_layout.addWidget(self.saving_button)


        Sample_layout.addWidget(self.sample_picture_label)
        Sample_layout.addWidget(self.sample_picture_label2)

        Panel_layout.addWidget(self.Mask_value_label2)
        Panel_layout.addWidget(self.element_name_label)
        Panel_layout.addWidget(self.previous_element_button)
        Panel_layout.addWidget(self.next_element_button)
        Panel_layout.addWidget(self.use_for_mask_button)
        Panel_layout.addWidget(self.quantify_button)

        Results_layout.addWidget(self.Cursor_data_label)
        Results_layout.addWidget(Color("transparent"))
        Results_layout.addWidget(self.X_label)
        Results_layout.addWidget(self.X_value_label)
        Results_layout.addWidget(Color("transparent"))
        Results_layout.addWidget(self.Y_label)
        Results_layout.addWidget(self.Y_value_label)
        Results_layout.addWidget(Color("transparent"))
        Results_layout.addWidget(self.Value_label)
        Results_layout.addWidget(self.Value_value_label)
        Results_layout.addWidget(Color("transparent"))
        Results_layout.addWidget(Color("transparent"))
        Results_layout.addWidget(Color("transparent"))
        Results_layout.addWidget(self.Mean_label)
        Results_layout.addWidget(self.Mean_value_label)
        Results_layout.addWidget(Color("transparent"))
        Results_layout.addWidget(self.Median_label)
        Results_layout.addWidget(self.Median_value_label)
        Results_layout.addWidget(Color("transparent"))
        Results_layout.addWidget(self.Min_label)
        Results_layout.addWidget(self.Min_value_label)
        Results_layout.addWidget(Color("transparent"))
        Results_layout.addWidget(self.Max_label)
        Results_layout.addWidget(self.Max_value_label)
        Results_layout.addWidget(Color("transparent"))
        Results_layout.addWidget(self.Mask_label)
        Results_layout.addWidget(self.Mask_value_label)
        Results_layout.addWidget(Color("transparent"))
        

        widget = QWidget()
        widget.setLayout(pagelayout)
        self.setCentralWidget(widget)
    
