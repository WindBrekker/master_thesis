def Quantify(self):
    for f in self.folders_names:
        self.folder = f
        
        #Searching for prename
        file_names = os.listdir(Path(os.path.join(self.Main_Folder_Path,f)))
        first_file = file_names[0]
        splitted_prename = first_file.rsplit("_",1)
        self.prename = splitted_prename[0]
        print("prename: "+ str(self.prename))
        self.separator = first_file.split(self.prename)[1].split(self.elements_in_nodec[0])[0]
        print(self.separator)
        
        #calculating livetime with zeropeak
        zeropeak_matrix = utils.file_to_list(Path(os.path.join(self.Main_Folder_Path,f,f"{self.prename}{self.separator}{self.zeropeak_name}.txt")))
        self.livetime_matrix = utils.LT_calc(zeropeak_matrix,self.zeropeak_dict["a"],self.zeropeak_dict["b"]) 
        
        if not Path(os.path.join(self.Main_Folder_Path,f"{f}_output")).exists():
            Path(os.path.join(self.Main_Folder_Path,f"{f}_output")).mkdir()

        utils.output_to_file(self.livetime_matrix, Path(os.path.join(self.Main_Folder_Path,f"{f}_output",f"{self.prename}_livetime_map"))) 
        self.mask_map = utils.mask_creating(self.elements_in_nodec[0],self.Main_Folder_Path,f,self.prename,self.treshold,self.color_of_heatmap,self.separator)
        self.antimask_map = utils.antimask_creating(self.elements_in_nodec[0],self.Main_Folder_Path,f,self.prename,self.treshold,self.color_of_heatmap,self.separator)

        #Create folder for outputs, if doesnt exist one yet
        if not Path(os.path.join(self.Main_Folder_Path,"temporary")).exists():
            Path(os.path.join(self.Main_Folder_Path,"temporary")).mkdir()
        if not Path(os.path.join(self.Main_Folder_Path,f"{self.folder}_output")).exists():
            Path(os.path.join(self.Main_Folder_Path,f"{self.folder}_output")).mkdir()
        if not Path(os.path.join(self.Main_Folder_Path,"temporary",f"{self.folder}_output")).exists():
            Path(os.path.join(self.Main_Folder_Path,"temporary",f"{self.folder}_output")).mkdir() 
        self.temporary_folder = Path(os.path.join(self.Main_Folder_Path,"temporary",f"{self.folder}_output"))
        
        
        sm = []
        scater_tab = []
        scater_tab = utils.file_to_list(os.path.join(self.Main_Folder_Path,self.folder,f"{self.prename}{self.separator}{self.scater_name}.txt"))
        print(len(scater_tab))
        print(len(self.livetime_matrix))
        
        for i in range(len(scater_tab)):
            for j in range(len(scater_tab[0])):
                scater_tab[i][j] = scater_tab[i][j] / float(self.livetime_matrix[i][j])
        
        
        
        sm_livetime = [[0 for j in range(len(scater_tab[0]))]for i in range(len(scater_tab))]
        antimask_scater = [[0 for j in range(len(scater_tab[0]))]for i in range(len(scater_tab))]
        antimask_scater_mask = [[0 for j in range(len(scater_tab[0]))]for i in range(len(scater_tab))]
        antimask_scater_masked = [[0 for j in range(len(scater_tab[0]))]for i in range(len(scater_tab))]
        
        for i in range(len(scater_tab)):
            for j in range(len(scater_tab[0])):
                antimask_scater[i][j] = float(scater_tab[i][j]) * float(self.antimask_map[i][j])
                
        scater_treshold = np.min(scater_tab)
        for i in range(len(antimask_scater)):
            for j in range(len(antimask_scater[0])):
                if self.antimask_map[i][j] and antimask_scater[i][j] < (float(1.25) * float(scater_treshold)):
                    antimask_scater_mask[i][j] = 1 
                else:
                    antimask_scater_mask[i][j] = 0
        

        utils.output_to_file(antimask_scater_mask,os.path.join(self.temporary_folder,"antimask_scater_mask"))
        antimask_sum = 0      
        iteration_antimask = 0     
        for i in range(len(antimask_scater)):
            for j in range(len(antimask_scater[0])):
                antimask_scater_masked[i][j] = float(antimask_scater_mask[i][j]) * float(antimask_scater[i][j])
                if antimask_scater_mask[i][j]:
                    antimask_sum += antimask_scater_masked[i][j]
                    iteration_antimask += 1
        
        antimask_mean = antimask_sum/iteration_antimask
        
        print(antimask_mean)
        
        plt.imshow(antimask_scater_mask,cmap=self.color_of_heatmap, interpolation="nearest")
        plt.savefig("antimask_plot.png")
        
        
        
        for i in range(len(scater_tab)):
            for j in range(len(scater_tab[0])):
                if float(scater_tab[i][j])-float(antimask_mean) > 0:
                    sm_livetime[i][j] = (float(scater_tab[i][j])-float(antimask_mean))
                else:
                    sm_livetime[i][j] = 0

        sm = utils.SampSM_calc(sm_livetime,self.scater_dict["a"],self.scater_dict["b"])
        print(np.median(sm))
        sm_masked = [[0 for j in range(len(sm[0]))] for i in range(len(sm))]
        for i in range(len(scater_tab)):
            for j in range(len(scater_tab[0])):
                sm_masked[i][j] = sm[i][j] * self.mask_map[i][j]
        utils.output_to_file(sm_masked,os.path.join(self.temporary_folder,"sample_mass_noc")) 
            
        
        #loop for every element in all folders
        for key in self.Z_number_per_element_dict:
                element = key
                
                #check if there is data for the element in this folder
                if file_exists(os.path.join(self.Main_Folder_Path,self.folder, f"{self.prename}{self.separator}{element}.txt")):
                    K_i = float(self.K_value_per_element_dict[element])
                    counts_data = os.path.join(self.Main_Folder_Path, self.folder,f"{self.prename}{self.separator}{element}.txt")
                    counts_table = utils.file_to_list(counts_data)
                    table_of_smi = [[0 for j in range(len(counts_table[0]))]for i in range(len(counts_table))]
                    

                    
                    for i in range(len(counts_table)):

                        for j in range(len(counts_table[0])):
                            table_of_smi[i][j] = (((float(counts_table[i][j]) * float(self.mask_map[i][j])))/ float(self.livetime_matrix[i][j])/ (float(K_i)))
                    utils.output_to_file(table_of_smi,os.path.join(self.temporary_folder,f"{element}_element_mass_noc"))                 
                            
                    

                    Ci_table = [[0 for j in range(len(sm[0]))] for i in range(len(sm))]
                    Ci_table_no_heatpoints = [[0 for j in range(len(sm[0]))] for i in range(len(sm))]
                    lambda_factor = [[0 for j in range(len(sm[0]))] for i in range(len(sm))]
                    counter = 0
                    number = 0
                    Ci_table_sum = 0
                    lambda_factor_sum = 0
                    print(len(sm))
                    print(len(sm[0]))
                    for i in range(len(sm)):
                        for j in range(len(sm[0])):
                            if table_of_smi[i][j] != 0:
                                lambda_factor[i][j] = utils.lambda_factor(sm[i][j], int(self.Z_number_per_element_dict[element]),float(self.energy_per_element_dict[element]),self.concentration_per_element_dict )
                                if sm[i][j] > 0.3*(np.median(sm)) and table_of_smi[i][j] >= 0 :
                                    Ci_table[i][j] = (table_of_smi[i][j] * lambda_factor[i][j] / sm[i][j])
                                    print(number)
                                    print(number*100/(len(sm)*len(sm[0])))
                                    number+=1
                                    
                                else:
                                    Ci_table[i][j] = 0
                                    print("Tu jest ci zero!")
                                    # print("smi: " + str(table_of_smi[i][j]) + " Lambda: " + str(lambda_factor[i][j]) + " sm: " + str(sm[i][j]))
                                counter +=1
                                Ci_table_sum += Ci_table[i][j]
                                lambda_factor_sum += lambda_factor[i][j]
                                
                            else:
                                continue
                    lambda_average_factor = lambda_factor_sum/counter
                    Ci_average_factor = Ci_table_sum/counter
                    
        
                    
                    for i in range(len(sm)):
                        for j in range(len(sm[0])):
                            if Ci_table[i][j] > 10*float(Ci_average_factor):
                                Ci_table_no_heatpoints[i][j] = 0   
                            else:
                                Ci_table_no_heatpoints[i][j] = Ci_table[i][j]    
                                
                    
                    utils.output_to_file(Ci_table_no_heatpoints,os.path.join(self.Main_Folder_Path,"temporary",f"{self.folder}_output",f"{self.prename}_{element}_Ci_no_heatpoints"))               
                    
                    utils.output_to_file(lambda_factor,os.path.join(self.Main_Folder_Path,f"{self.folder}_output",f"{self.prename}_{element}_lambda"))
                    with open( os.path.join(self.Main_Folder_Path,f"{self.folder}_output", f"lambda_Ci_average.txt"), "a") as f:
                        f.write(f'element:  {element},  average lambda: {format(lambda_average_factor, ".2e")},    average Ci [g/g]: {format(Ci_average_factor, ".2e")}, \n')                        
                    utils.output_to_file(Ci_table,os.path.join(self.Main_Folder_Path,"temporary",f"{self.folder}_output",f"{self.prename}_{element}_Ci"))
                    
                                            

                                
                else:
                    continue  

        
                            
    self.chosen_folder = self.Prefere_folder.currentText()
    self.confirm_names_button.disconnect()
    self.confirm_names_button.setEnabled(False)
    self.previous_element_button.disconnect()
    self.previous_element_button.clicked.connect(self.previous_element_final)
    self.next_element_button.disconnect()
    self.next_element_button.clicked.connect(self.next_element_final)
    self.quantify_button.disconnect()
    self.quantify_button.setText("Go back")
    self.quantify_button.clicked.connect(self.Back_to_quantify)
    self.Prefere_folder.activated.disconnect()
    self.Prefere_folder.activated.connect(self.new_prefered_folder)
    
    iteration = 0
    while not Path(os.path.join(self.Main_Folder_Path,"temporary",f"{self.chosen_folder}_output",f"{self.prename}_{self.elements_in_nodec[iteration]}_Ci.txt")).exists():
        iteration += 1
    
    
    plt.imshow(utils.file_to_list(os.path.join(self.Main_Folder_Path,"temporary",f"{self.chosen_folder}_output",f"{self.prename}_{self.elements_in_nodec[iteration]}_Ci.txt")), cmap=self.color_of_heatmap, interpolation="nearest")
    plt.title("Concentration map")
    plt.colorbar()
    plt.savefig(os.path.join(self.Main_Folder_Path,"temporary",f"{self.chosen_folder}_output",f"{self.prename}_{self.elements_in_nodec[iteration]}_Ci.png"))
    plt.close()
    
    plt.imshow(utils.file_to_list(os.path.join(self.Main_Folder_Path,"temporary",f"{self.chosen_folder}_output",f"{self.prename}_{self.elements_in_nodec[iteration]}_Ci_no_heatpoints.txt")), cmap=self.color_of_heatmap, interpolation="nearest")
    plt.title("Concentration map without heatpoints")
    plt.colorbar()
    plt.savefig(os.path.join(self.Main_Folder_Path,"temporary",f"{self.chosen_folder}_output",f"{self.prename}_{self.elements_in_nodec[iteration]}_Ci_no_heatpoints.png"))
    plt.close()
    
    
    self.sample_pixmap = QPixmap(os.path.join(self.Main_Folder_Path,"temporary",f"{self.chosen_folder}_output",f"{self.prename}_{self.elements_in_nodec[iteration]}_Ci.png"))
    self.sample_picture_label.setPixmap(self.sample_pixmap)
    
    self.sample_pixmap2 = QPixmap(os.path.join(self.Main_Folder_Path,"temporary",f"{self.chosen_folder}_output",f"{self.prename}_{self.elements_in_nodec[iteration]}_Ci_no_heatpoints.png"))
    self.sample_picture_label2.setPixmap(self.sample_pixmap2)
    
    element_table_not_masked = np.array(utils.file_to_list(os.path.join(self.Main_Folder_Path,"temporary",f"{self.chosen_folder}_output",f"{self.elements_in_nodec[iteration]}_element_mass_noc.txt")))

    self.element_table = element_table_not_masked[element_table_not_masked != 0]
    self.Mean_value_label.setText(str(np.average(self.element_table)))
    self.Median_value_label.setText(str(np.median(self.element_table)))
    self.Min_value_label.setText(str(np.min(self.element_table)))
    self.Max_value_label.setText(str(np.max(self.element_table)))
    
    self.saving_button.setEnabled(True)                                      
    
def Confirmed_saving(self):
    self.quantify_button.setEnabled(True)
    self.use_for_mask_button.setEnabled(True)        
    self.next_element_button.setEnabled(True)
    self.previous_element_button.setEnabled(True)      

def file_to_list(input):
    try:
        converted_list = np.loadtxt(input,delimiter=';')
        # print(converted_list)
        # print(type(converted_list[0]))
        # print(type(converted_list[0][0]))
        return converted_list
    except:
        print("Couldn't find data")
        print(input)
        return None

def LT_calc(input,a,b):
#zeropeak

    output = []
    for i in range (len(input)):
        output.append([(((float(a)* float(input[i][j]) + float(b)))) for j in range(len(input[i]))]) #Livetime [s]  
    return output

def SampSM_calc(input,a,b):
#scatter

    output = [[0 for j in range(len(input[0]))]for i in range(len(input))]
    for i in range (len(input)):
        for j in range(len(input[i])):
            if ((float(a) * float(input[i][j])) + float(b)) > 0:
                output[i][j] = (float(a) * float(input[i][j])) + float(b)#g/cm^2
               # print("Zero dla: " + str(input[i][j]))

    return output

def output_to_file(input, output):
    # open file in write mode
    with open(f"{output}.txt", "w") as f:
        # loop through 2D list
        for row in input:
            formatted_row = [format('{:.2e}'.format(x)) for x in row]
            # write formatted row to file, separated by commas and ending with newline character
            f.write(','.join(formatted_row) + '\n')

def absorption_coefficient(sample_dict,Ee):
        u_E = 0
        for key in sample_dict:
            ui_E = xr.CS_Total_CP(key,Ee)
            u_E += ui_E*float(sample_dict[key])
        return (u_E) #jednostka cm^2/g

def lambda_factor(rho_D,Z,Eeffi,sample_dict):
    
    phi_in = math.radians(50)
    phi_out = math.radians(50)
    
    Eijk = xr.LineEnergy(Z,xr.KA1_LINE)
    u_Eijk = absorption_coefficient(sample_dict,Eijk)
    u_Eeffi = absorption_coefficient(sample_dict,Eeffi)
    #wczytujemy Eeffi z pliczku input i Eijk z funcji xr.LineEnergy(Z,xr.KA1_LINE)
    
    denominator = rho_D*((u_Eeffi/(math.sin(phi_in)))+(u_Eijk/(math.sin(phi_out))))
    numerator = 1-(math.exp(-1*(denominator)))
    if denominator == 0:
        correction_factror = 0
    else: 
        correction_factror = denominator/numerator


    return correction_factror

def mask_creating(element,Path, folder, prename,treshold,color,separator):
    # wczytywanie mapy do maski
        element_for_mask = element
        file_path = os.path.join(Path, folder, f"{prename}{separator}{element_for_mask}.txt")
        table_of_mask = file_to_list(file_path)        

        maxof_masktable = np.max(table_of_mask)
        # print("max of table")
        # print(maxof_masktable)
        procent = (float(treshold)/100)
        mask = [
            [0 for j in range(len(table_of_mask[0]))] for i in range(len(table_of_mask))
        ]
        for i in range(len(table_of_mask)):
            for j in range(len(table_of_mask[0])):
                if table_of_mask[i][j] < (procent * maxof_masktable):
                    mask[i][j] = 0  
                else:
                    mask[i][j] = 1
        output_to_file(mask, os.path.join(Path,f"{folder}_output", f"{prename}_mask"))           
        
        
        plt.imshow(mask, cmap=color, interpolation="nearest")
        plt.title("Mask heatmap")
        plt.savefig(os.path.join(Path,f"{folder}_output","mask.png"))
        plt.close()
        plt.imshow(table_of_mask, cmap=color, interpolation="nearest")
        plt.title("Mask number of counts")
        plt.colorbar()
        plt.savefig(os.path.join(Path,f"{folder}_output","mask_noc.png"))
        plt.close()
        return mask
    
def antimask_creating(element,Path, folder, prename,treshold,color,separator):
    # wczytywanie mapy do maski
        element_for_mask = element
        file_path = os.path.join(Path, folder, f"{prename}{separator}{element_for_mask}.txt")
        table_of_mask = file_to_list(file_path)        

        maxof_masktable = np.max(table_of_mask)
        # print("max of table")
        # print(maxof_masktable)
        procent = (float(treshold)/100)
        mask = [
            [0 for j in range(len(table_of_mask[0]))] for i in range(len(table_of_mask))
        ]
        for i in range(len(table_of_mask)):
            for j in range(len(table_of_mask[0])):
                if table_of_mask[i][j] < (procent * maxof_masktable):
                    mask[i][j] = 1  
                else:
                    mask[i][j] = 0
        output_to_file(mask, os.path.join(Path,f"{folder}_output", f"{prename}_antimask"))           
        
        
        plt.imshow(mask, cmap=color, interpolation="nearest")
        plt.title("Antimask heatmap")
        plt.savefig(os.path.join(Path,f"{folder}_output","antimask.png"))
        plt.close()
        plt.imshow(table_of_mask, cmap=color, interpolation="nearest")
        plt.title("Antimask number of counts")
        plt.colorbar()
        plt.savefig(os.path.join(Path,f"{folder}_output","antimask_noc.png"))
        plt.close()
        return mask
