import os
import numpy as np
import pandas as pd

def process_timing_data(data):
    timingpoints = []
    prev_uninherited_str = None
    prev_inherited_str = None
    np.set_printoptions(precision=10, suppress=True)
    # for d in data:
    #     print(d[-16:])

    for array in data:
        # print(array)
        # Extract the last 16 elements
        last_16_elements = array[-16:]
        
        # Divide into uninherited and inherited timing points
        uninherited_points = last_16_elements[8:]
        inherited_points = last_16_elements[:8]


        # # Convert lists to tuples for comparison
        # uninherited_tuple = uninherited_points
        # inherited_tuple = inherited_points

        # Modify the second value of inherited points
        inherited_points[1] = 0-float(inherited_points[1])

        # Convert elements to strings
        # Convert points to lists of strings
        uninherited_str_list = [str(value) for value in uninherited_points]
        inherited_str_list = [str(value) for value in inherited_points]

        # Join the lists into comma-separated strings
        uninherited_str = ",".join(uninherited_str_list)
        inherited_str = ",".join(inherited_str_list)

        # Append uninherited timing points if different from previous
        if uninherited_str != prev_uninherited_str:
            timingpoints.append(uninherited_str)
            prev_uninherited_str = uninherited_str

        # Append inherited timing points if different from previous
        # but only if uninherited and inherited are both different
        if inherited_str != prev_inherited_str:
            timingpoints.append(inherited_str)
            prev_inherited_str = inherited_str

    return timingpoints




def load_and_print_npy_data(df):
    for index, row in df.iterrows():
        # Construct the full path to the .npy file
        folder_path = os.path.join("processed-beatmaps", f"{row['audio']}-b.npy")
        
        # Load the .npy file into a NumPy array
        if os.path.exists(folder_path):
            data_array = np.load(folder_path)
            
            # Print the loaded data
            print(f"Loaded data from {folder_path}:")
            # print(data_array)
            timingpoint = np.array(process_timing_data(data_array))
            print(timingpoint)
        else:
            print(f"File {folder_path} does not exist.")
            return None

    
