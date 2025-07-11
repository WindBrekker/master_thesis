
import numpy as np
import matplotlib.pyplot as plt
import os
import csv
from scipy.stats import shapiro


element_stats = {
    "Ca": {"mean": 3.30e-01, "std": 1.17e-03},
    "Cl": {"mean": 2.52e+00, "std": 2.09e-03},
    "Cr": {"mean": 1.35e-01, "std": 1.77e-04},
    "Cu": {"mean": 1.49e-01, "std": 2.21e-04},
    "Fe": {"mean": 4.93e-01, "std": 1.40e-03},
    "K":  {"mean": 5.01e+00, "std": 4.67e-03},
    "Mg": {"mean": 8.83e-01, "std": 1.84e-03},
    "Na": {"mean": 3.19e+00, "std": 6.92e-03},
    "P":  {"mean": 5.55e+00, "std": 5.37e-03},
    "S":  {"mean": 4.24e+00, "std": 3.84e-03},
    "Zn": {"mean": 2.00e-01, "std": 2.85e-04},
}


def read_matrix(file_path):
    """Reads a matrix and returns a flattened array excluding zeros."""
    matrix = np.loadtxt(file_path, delimiter=',')
    flattened = matrix.flatten()
    return flattened[flattened != 0]

def analyze_data(data_array):
    """Returns mean, std, and Shapiro-Wilk normality test p-value."""
    mean_val = np.mean(data_array)
    std_val = np.std(data_array)
    return mean_val, std_val

def main():
    for pierwiastek in ['Ca', 'Cl', 'Cu', 'Fe', 'K', 'Mg', 'Na', 'P', 'S', 'Zn']:
        print(f"Processing element: {pierwiastek}")
        folder_path = f"C:\\Users\\wikto\\OneDrive\\Pulpit\\magisterka\\{pierwiastek}_tornado"
        file_names = sorted([f for f in os.listdir(folder_path) if f.endswith('.txt')])

        data = []
        labels = []
        stats_rows = [("File", "Mean", "Std Dev", "Shapiro p-value", "Looks Normal?")]

        for fname in file_names:
            full_path = os.path.join(folder_path, fname)
            values = read_matrix(full_path)

            if len(values) == 0:
                continue

            mean, std = analyze_data(values)
            stats_rows.append((fname, mean, std))

            data.append(values)
            labels.append(fname)

        # Save stats to CSV
        output_csv = f"C:\\Users\\wikto\\OneDrive\\Pulpit\\magisterka\\Polyx\\{pierwiastek}_stats.csv"
        with open(output_csv, mode='w', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            writer.writerows(stats_rows)

if __name__ == '__main__':
    main()
