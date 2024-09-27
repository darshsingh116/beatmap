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
            y, sr = librosa.load(file_path, sr=22000)
            # print(y)
            # print(sr)
        except FileNotFoundError:
            print(f"File {file_path} not found.")
            continue

        # Define custom frame size and hop length
        frame_size = 221  # Frame size (n_fft)
        hop_length = 220  # Hop length (number of samples between successive frames)
        #doing above will create 1mff per 10ms audio as sampling rate is 22000 and hop size is 220
        
        # Compute MFCCs with the specified frame size and hop length
        mfcc = librosa.feature.mfcc(y=y, sr=sr, n_mfcc=13, n_fft=frame_size, hop_length=hop_length,n_mels=40)
        # Extract Chroma features
        chroma = librosa.feature.chroma_cqt(y=y, sr=sr, hop_length=hop_length, n_chroma=12)
        
        # Combine features
        combined_features = np.concatenate((mfcc, chroma), axis=0)

        combined_features = np.transpose(combined_features)
        
        # Convert to float32 to save memory
        combined_features = combined_features.astype(np.float32)
        print(len(combined_features))
        print(combined_features.shape)
        # print(len(mfcc))
        # print("~~~~")
        # chunks = create_chunks_from_mfcc(mfcc)


        # Construct the save path
        save_path = os.path.join(processed_dir, f"{row['audio']}-a.npy")
        
        # Save the MFCC features as a .npy file
        np.save(save_path, combined_features)
        # print(f"Saved: {save_path}")



def process_audio(row, processed_dir):
    try:
        file_path = os.path.join(archive_path, "train", row['folder'], "audio.opus")
        
        try:
            y, sr = librosa.load(file_path, sr=22000)
        except FileNotFoundError:
            print(f"File {file_path} not found.")
            return
        
        # Define custom frame size and hop length
        frame_size = 221  # Frame size (n_fft)
        hop_length = 220  # Hop length (number of samples between successive frames)
        #doing above will create 1mffc per 10ms audio as sampling rate is 22000 and hop size is 220
        
        # Compute MFCCs with the specified frame size and hop length
        mfcc = librosa.feature.mfcc(y=y, sr=sr, n_mfcc=13, n_fft=frame_size, hop_length=hop_length,n_mels=40)
        # Extract Chroma features
        # chroma = librosa.feature.chroma_cqt(y=y, sr=sr, hop_length=hop_length, n_chroma=12)
  
        # combined_features = np.concatenate((mfcc, chroma), axis=0)
        # combined_features = np.transpose(combined_features)
        mfcc = np.transpose(mfcc)
        # Convert to float32 to save memory
        # combined_features = combined_features.astype(np.float32)
        combined_features = mfcc.astype(np.float32)
        
        # chunks = create_chunks_from_mfcc(mfcc)


        # Construct the save path
        save_path = os.path.join(processed_dir, f"{row['audio']}-a.npy")
        
        # Save the MFCC features as a .npy file
        np.save(save_path, combined_features)
        # print(f"Saved: {save_path}")
    except:
        print("error")

def preprocess_and_save_audio_in_parallel(df):
    # Directory where processed files will be saved
    processed_dir = os.path.join(os.getcwd(), 'processed-audio')
    
    # Check if the directory exists, if not, create it
    os.makedirs(processed_dir, exist_ok=True)
    
    # Use joblib's Parallel and delayed to parallelize the processing
    Parallel(n_jobs=3)(delayed(process_audio)(row, processed_dir) for index, row in df.iterrows())






# Example usage with your DataFrame
# df = pd.read_csv('your_data.csv')  # Load your DataFrame if not already loaded
# preprocess_and_save_audio(df)


def openl3_preprocess_and_save_audio_in_parallel(df):
    # Directory where processed files will be saved
    processed_dir = os.path.join(os.getcwd(), 'processed-audio')
    
    # Check if the directory exists, if not, create it
    os.makedirs(processed_dir, exist_ok=True)
    
    # Use joblib's Parallel and delayed to parallelize the processing
    Parallel(n_jobs=-1)(delayed(openl3_process_audio)(row, processed_dir) for index, row in df.iterrows())


import openl3
import soundfile as sf

def openl3_process_audio(row, processed_dir):
    try:
        # Construct the file path for the audio
        file_path = os.path.join(archive_path, "train", row['folder'], "audio.opus")
        
        try:
            # Extract audio features directly from the audio file using OpenL3
            embeddings, timestamps = openl3.get_audio_embedding_from_file(file_path, hop_size=0.01, content_type="music")
        except FileNotFoundError:
            print(f"File {file_path} not found.")
            return
        
        # Construct the save path
        save_path = os.path.join(processed_dir, f"{row['audio']}-a.npy")
        
        # Save the OpenL3 embeddings (features) as a numpy file
        np.save(save_path, embeddings)
        print(f"Saved: {save_path}")
        
    except Exception as e:
        print(f"Error processing file {file_path}: {e}")


def openl3_preprocess_and_save_audio(df):
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
            # Load the audio file
            audio, sr = sf.read(file_path,samplerate=22050)
            
            # Extract audio features using OpenL3
            embeddings, timestamps = openl3.get_audio_embedding(audio, sr, hop_size=0.01, content_type="music")
            
            # Convert to float32 to save memory
            embeddings = embeddings.astype(np.float32)
            
            # Downsample the embeddings
            downsampled_embeddings = embeddings[::10]
            downsampled_timestamps = timestamps[::10]
        except FileNotFoundError:
            print(f"File {file_path} not found.")
            continue

        # Construct the save path
        save_path = os.path.join(processed_dir, f"{row['audio']}-a.npy")
         # Save the downsampled embeddings and timestamps
        np.save(save_path + '_embeddings.npy', downsampled_embeddings)
        np.save(save_path + '_timestamps.npy', downsampled_timestamps)
        print(f"Saved: {save_path}_embeddings.npy and {save_path}_timestamps.npy")
        # Save the MFCC features as a .npy file
        # np.save(save_path, embeddings)
        # print(f"Saved: {save_path}")