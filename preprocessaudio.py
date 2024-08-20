import os
import librosa
import numpy as np
from dotenv import load_dotenv
load_dotenv()
archive_path = os.getenv('ARCHIVE_PATH')

def preprocess_and_save_audio(df):
    # Directory where processed files will be saved
    processed_dir = os.path.join(os.getcwd(), 'processed-audio')
    
    # Check if the directory exists, if not, create it
    if not os.path.exists(processed_dir):
        os.makedirs(processed_dir)
    
    for index, row in df.iterrows():
        # Construct the file path from the folder and audio fields
        file_path = os.path.join(archive_path,"train", row['folder'], "audio.opus")
        
        # Load the audio file
        try:
            y, sr = librosa.load(file_path, sr=None)
        except FileNotFoundError:
            print(f"File {file_path} not found.")
            continue

        # Extract MFCC features
        mfcc = librosa.feature.mfcc(y=y, sr=sr, n_mfcc=13)
        # mfcc = np.array(mfcc)
        # mfcc = np.transpose(mfcc)
        
        # Construct the save path
        save_path = os.path.join(processed_dir, f"{row['audio']}.npy")
        
        # Save the MFCC features as a .npy file
        np.save(save_path, mfcc)
        print(f"Saved: {save_path}")

# Example usage with your DataFrame
# df = pd.read_csv('your_data.csv')  # Load your DataFrame if not already loaded
# preprocess_and_save_audio(df)