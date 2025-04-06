import numpy as np
import os
from pathlib import Path


def read_file(input):
    
    txt_path = input
    
    try:
        if os.path.exists(txt_path):
            with open(txt_path, 'r') as file:
                first_line = file.readline()
                delimiter = ';' if ';' in first_line else ','
            converted_array = np.loadtxt(txt_path, delimiter=delimiter)
            print(f"Delimiter used: {delimiter}")
            print(f"Data shape: {converted_array.shape}")
            return np.array(converted_array)
        else:
            print(f"File not found: {txt_path}")
    except Exception as e:
        print(f"Couldn't find data: {e}")
        print(input)
        return None

def sum_zeropeak(data1, data2, data3):
    # Check if all data arrays are of the same length
    if len(data1) != len(data2) or len(data1) != len(data3):
        raise ValueError("All input arrays must have the same length.")

    # Calculate the sum of the three data arrays
    summed_data = data1 + data2 + data3
    print(data1[0:10])
    print(data2[0:10])
    print(data3[0:10])
    print(summed_data[0:10])

    return summed_data


file_1 = "tkanka_F1.txt"
file_2 = "tkanka_F2.txt"
file_3 = "tkanka_F3.txt"

data1 = read_file(file_1)
data2 = read_file(file_2)
data3 = read_file(file_3)

# Assuming data1, data2, and data3 are numpy arrays of the same length

sum_zeropeak_result = sum_zeropeak(data1, data2, data3)
np.savetxt(f"tkanka_zeropeak.txt", sum_zeropeak_result, fmt='%.2e', delimiter=';')



