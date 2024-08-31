import os
import librosa
import numpy as np
from audio import *
from joblib import Parallel, delayed
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
            y, sr = librosa.load(file_path, sr=22050)
            # print(y)
            # print(sr)
        except FileNotFoundError:
            print(f"File {file_path} not found.")
            continue

        # Define custom frame size and hop length
        frame_size = 2048  # Frame size (n_fft)
        hop_length = 512   # Hop length (number of samples between successive frames)

        # Compute MFCCs with the specified frame size and hop length
        mfcc = librosa.feature.mfcc(y=y, sr=sr, n_mfcc=13, n_fft=frame_size, hop_length=hop_length)
        mfcc = np.array(mfcc)
        mfcc = np.transpose(mfcc)
        chunks = create_chunks_from_mfcc(mfcc)
        # Construct the save path
        save_path = os.path.join(processed_dir, f"{row['audio']}-a.npy")
        
        # Save the MFCC features as a .npy file
        np.save(save_path, chunks)
        # print(f"Saved: {save_path}")



def process_audio(row, processed_dir):
    try:
        file_path = os.path.join(archive_path, "train", row['folder'], "audio.opus")
        
        try:
            y, sr = librosa.load(file_path, sr=22050)
        except FileNotFoundError:
            print(f"File {file_path} not found.")
            return
        
        # Define custom frame size and hop length
        frame_size = 2048  # Frame size (n_fft)
        hop_length = 512   # Hop length (number of samples between successive frames)
        
        # Compute MFCCs with the specified frame size and hop length
        mfcc = librosa.feature.mfcc(y=y, sr=sr, n_mfcc=13, n_fft=frame_size, hop_length=hop_length)
        mfcc = np.transpose(mfcc)
        chunks = create_chunks_from_mfcc(mfcc)

        
        # Construct the save path
        save_path = os.path.join(processed_dir, f"{row['audio']}-a.npy")
        
        # Save the MFCC features as a .npy file
        np.save(save_path, chunks)
        print(f"Saved: {save_path}")
    except:
        print("error")

def preprocess_and_save_audio_in_parallel(df):
    # Directory where processed files will be saved
    processed_dir = os.path.join(os.getcwd(), 'processed-audio')
    
    # Check if the directory exists, if not, create it
    os.makedirs(processed_dir, exist_ok=True)
    
    # Use joblib's Parallel and delayed to parallelize the processing
    Parallel(n_jobs=-1)(delayed(process_audio)(row, processed_dir) for index, row in df.iterrows())






# Example usage with your DataFrame
# df = pd.read_csv('your_data.csv')  # Load your DataFrame if not already loaded
# preprocess_and_save_audio(df)