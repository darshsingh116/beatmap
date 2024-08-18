import os
import numpy as np

def load_mfcc_data_from_npy_folder(folder_path):
    """
    Load MFCC data stored as .npy files from a specified folder and store them in memory.
    
    Parameters:
    - folder_path: str, path to the folder containing .npy files.
    
    Returns:
    - mfcc_data: list of numpy arrays, each containing MFCC features from a .npy file.
    """
    mfcc_data = []
    
    # List all files in the folder
    for filename in os.listdir(folder_path):
        if filename.endswith('.npy'):
            file_path = os.path.join(folder_path, filename)
            
            # Load the .npy file
            data = np.load(file_path)
            
            # Append the loaded data to the list
            mfcc_data.append(data)
    
    return mfcc_data
