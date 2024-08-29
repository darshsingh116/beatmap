import os
import numpy as np
import pandas as pd

def process_timing_data(data):
    timingpoints = []
    prev_uninherited = None
    prev_inherited = None

    for array in data:
        # Extract the last 16 elements
        last_16_elements = array[-16:]
        
        # Divide into uninherited and inherited timing points
        uninherited_points = last_16_elements[8:]
        inherited_points = last_16_elements[:8]


        # Convert lists to tuples for comparison
        uninherited_tuple = tuple(uninherited_points)
        inherited_tuple = tuple(inherited_points)

        # Modify the second value of inherited points
        x = float(inherited_points[1])
        inherited_points[1] = (-(100 / x))

        # Convert elements to strings
        uninherited_points = [str(value) for value in uninherited_points]
        inherited_points = [str(value) for value in inherited_points]

        # Append uninherited timing points if different from previous
        if uninherited_tuple != prev_uninherited:
            timingpoints.append(uninherited_points)
            prev_uninherited = uninherited_tuple

        # Append inherited timing points if different from previous
        # but only if uninherited and inherited are both different
        if inherited_tuple != prev_inherited:
            if uninherited_tuple != prev_uninherited:
                timingpoints.append(uninherited_points)
                prev_uninherited = uninherited_tuple
            timingpoints.append(inherited_points)
            prev_inherited = inherited_tuple

    return timingpoints




def load_and_print_npy_data(df):
    for index, row in df.iterrows():
        # Construct the full path to the .npy file
        folder_path = os.path.join("processed-beatmaps", row["folder"], f"{row['audio']}.npy")
        
        # Load the .npy file into a NumPy array
        if os.path.exists(folder_path):
            data_array = np.load(folder_path)
            
            # Print the loaded data
            print(f"Loaded data from {folder_path}:")
            print(data_array)
        else:
            print(f"File {folder_path} does not exist.")
