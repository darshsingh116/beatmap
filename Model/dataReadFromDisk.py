import os
import tensorflow as tf
import numpy as np
import pandas as pd
from dotenv import load_dotenv

np.set_printoptions(precision=10, suppress=True)

#setting data path
load_dotenv()
project_path = os.getenv('PROJECT_PATH')

def load_df_from_csv():
    # Define the path to the CSV file in the processed metadata folder
    load_path = os.path.join(project_path,"processed-metadata", "processed-metadata.csv")
    
    # Check if the file exists before attempting to load it
    if os.path.exists(load_path):
        # Load the DataFrame from the CSV file
        df = pd.read_csv(load_path)
        print(f"DataFrame loaded from: {load_path}")
        return df
    else:
        print(f"File not found: {load_path}")
        return None


def load_all_beatmaps_from_df(df):
    # List to hold all loaded beatmap data
    all_beatmaps = []
    
    # Iterate over each row in the DataFrame
    for index, row in df.iterrows():
        # Extract the audio filename from the current row
        audio_filename = row['audio']
        
        # Define the path to the saved beatmap file based on the audio filename
        load_path = os.path.join(project_path,"processed-beatmaps", f"{audio_filename}-b.npy")
        
        # Load the NumPy array from disk with allow_pickle=True
        if os.path.exists(load_path):
            try:
                beatmap_data = np.load(load_path, allow_pickle=True)
                all_beatmaps.append(beatmap_data)
            except ValueError as e:
                print(f"Error loading {load_path}: {e}")
        else:
            print(f"File not found: {load_path}")
    
    return all_beatmaps



def load_all_beatmaps_and_audios_from_df(df):
    # Lists to hold all loaded beatmap and audio data
    all_beatmaps = []
    all_audios = []
    itr = 1
    total = len(df)
    # Iterate over each row in the DataFrame
    for index, row in df.iterrows():
        # Extract the audio filename from the current row
        audio_filename = row['audio']
        
        # Define the paths to the saved beatmap and audio files
        beatmap_path = os.path.join(project_path,"processed-beatmaps", f"{audio_filename}-b.npy")
        audio_path = os.path.join(project_path,"processed-audio", f"{audio_filename}-a.npy")
        
        # Check if both files exist and load them
        beatmap_data = None
        audio_data = None

        if os.path.exists(beatmap_path):
            try:
                beatmap_data = np.load(beatmap_path, allow_pickle=True)
            except ValueError as e:
                print(f"Error loading {beatmap_path}: {e}")
        
        if os.path.exists(audio_path):
            try:
                audio_data = np.load(audio_path, allow_pickle=True)
            except ValueError as e:
                print(f"Error loading {audio_path}: {e}")

        # If both files exist, append the data to their respective lists
        if beatmap_data is not None and audio_data is not None:
            all_beatmaps.append(beatmap_data)
            all_audios.append(audio_data)
        else:
            if beatmap_data is None:
                print(f"Beatmap file not found or failed to load: {beatmap_path}")
            if audio_data is None:
                print(f"Audio file not found or failed to load: {audio_path}")

        print(f"{itr}/{total}")
        itr += 1
    return all_beatmaps, all_audios




def process_audio_and_beatmap_for_model_single(metadata):
    # Define paths to the beatmap and audio files
    beatmap_path = os.path.join(project_path, "processed-beatmaps", f"{metadata['audio']}-b.npy")
    audio_path = os.path.join(project_path, "processed-audio", f"{metadata['audio']}-a.npy")

    # Load beatmap and audio data if files exist
    if not os.path.exists(beatmap_path):
        print(f"Beatmap file not found: {beatmap_path}")
        return None, None

    if not os.path.exists(audio_path):
        print(f"Audio file not found: {audio_path}")
        return None, None

    try:
        beatmap_data = np.load(beatmap_path, allow_pickle=True)
        audio_data = np.load(audio_path, allow_pickle=True)
    except ValueError as e:
        print(f"Error loading files: {e}")
        return None, None
    # for h in beatmap_data:
    #     print(h)
    # Initialize the processed lists
    processed_audio = []
    processed_beatmap = []

    # Iterate over each timeframe (20ms chunks with 10ms overlap)
    num_chunks = len(audio_data)
    beatmap_itr = 0

    input_footer = [float(metadata["bpm"]),float(metadata["total_length"])]+[float(x) for x in metadata[-9:]]

    for i in range(num_chunks):
        # fix_under_ten_ms = False
        if (beatmap_itr > 0) and beatmap_itr < len(beatmap_data):
            if beatmap_data[beatmap_itr][2] < beatmap_data[beatmap_itr-1][2]:
                raise ValueError(f"PARSING ERROR SOMEWHERE : Beatmap timestamp {beatmap_data[beatmap_itr][2]}ms is smaller than previous which is {beatmap_data[beatmap_itr-1][2]} in map {metadata['folder']}/{metadata['audio']}.osu")
        
        timestamp = i * 10  # Calculate the timestamp for this chunk in ms
        
        if (len(processed_beatmap) > 1) and (beatmap_itr > 0) and (beatmap_itr < len(beatmap_data)):
            if ((beatmap_data[beatmap_itr][2] - beatmap_data[beatmap_itr-1][2]) < 10) or (timestamp > beatmap_data[beatmap_itr][2]):
                if np.array_equal(processed_beatmap[-2], np.zeros_like(beatmap_data[0])):
                    processed_beatmap[-2] = processed_beatmap[-1]
                    processed_beatmap[-1] = beatmap_data[beatmap_itr]
                    # fix_under_ten_ms = True
                    # print(f"fixing under 10ms parts,beatmap_itr {beatmap_itr}, beatmap_data[beatmap_itr][2] {beatmap_data[beatmap_itr][2]} , beatmap_data[beatmap_itr-1][2] {beatmap_data[beatmap_itr-1][2]} ,  timestamp {timestamp}")
                    beatmap_itr += 1
                else:
                    a = (beatmap_data[beatmap_itr][2]- beatmap_data[beatmap_itr-1][2]) < 10
                    b = (timestamp >= beatmap_data[beatmap_itr][2])
                    raise  ValueError(f"Error on line 146 dataReadFromDisk.py Beatmap timestamp {beatmap_data[beatmap_itr][2]}ms in map {metadata['folder']}/{metadata['audio']}.osu {a} or {b}")


        # Add timestamp to the start of the audio chunk and footer on back
        audio_part = np.array(audio_data[i])
        audio_part = audio_part.flatten()
        audio_part = np.insert(audio_part,0,timestamp)
        audio_chunk = np.concatenate((audio_part, input_footer))
        processed_audio.append(audio_chunk)

        # Check for the timestamp of the current beatmap data
        if beatmap_itr < len(beatmap_data):
            beatmap_timestamp = beatmap_data[beatmap_itr][2]  # Assuming the timestamp is at index 3

            # If the audio chunk's timestamp overtakes the next beatmap timestamp, raise an error
            if beatmap_timestamp < timestamp and len(beatmap_data) > (beatmap_itr+1):
                raise ValueError(f"Audio timestamp {timestamp}ms has overtaken beatmap timestamp {beatmap_timestamp}ms in map {metadata['folder']}/{metadata['audio']}.osu")

            # Find the corresponding beatmap data within the 10ms window
            elif timestamp <= beatmap_timestamp < (timestamp + 10):
                beatmap_chunk = beatmap_data[beatmap_itr]
                # print(f"in beatmap_itr += 1 , timestamp is {timestamp} and beatmap time stamp is {beatmap_timestamp}")
                beatmap_itr += 1  # Move to the next beatmap entry
            else:
                # print(f"adding chunk with zero audio timestamp is {timestamp} and beatmap time stamp is {beatmap_timestamp}")
                beatmap_chunk = np.zeros_like(beatmap_data[0])  # Default to zeros if no match is found
        else:
            # print("beatmap finished adding zeroes")
            beatmap_chunk = np.zeros_like(beatmap_data[0])


        # if not fix_under_ten_ms:
        processed_beatmap.append(beatmap_chunk)

    return np.array(processed_audio), np.array(processed_beatmap)

def data_generator(processed_audio_list,processed_beatmap_list):
        for audio, beatmap in zip(processed_audio_list, processed_beatmap_list):
            yield (tf.convert_to_tensor(audio, dtype=tf.float32),
                    tf.convert_to_tensor(beatmap, dtype=tf.float32))


def create_dataset(processed_audio_list, processed_beatmap_list):
    # Generator function defined inside create_dataset
    def data_generator():
        for audio, beatmap in zip(processed_audio_list, processed_beatmap_list):
            yield (tf.convert_to_tensor(audio, dtype=tf.float32),
                    tf.convert_to_tensor(beatmap, dtype=tf.float32))

    # Create TensorFlow dataset
    dataset = tf.data.Dataset.from_generator(
        data_generator,
        output_signature=(
            tf.TensorSpec(shape=[None, 142], dtype=tf.float32),  # Variable length sequence with feature dimension 142
            tf.TensorSpec(shape=[None, 35], dtype=tf.float32)    # Variable length sequence with feature dimension 35
        )
    )
    

    return dataset

def process_audio_and_beatmap_for_model_all_and_save(df,chunk_size=2000):
    # Initialize empty arrays to store processed data
    processed_audio_list = []
    processed_beatmap_list = []

    save_path = os.path.join(project_path,"model-processed-data")
    if not os.path.exists(save_path):
        os.makedirs(save_path)
    itr=0
    # Iterate through the DataFrame
    for index, row in df.iterrows():
        processed_audio, processed_beatmap = process_audio_and_beatmap_for_model_single(row)

        # Append the processed data to lists
        processed_audio_list.append(processed_audio)
        processed_beatmap_list.append(processed_beatmap)

        # Save periodically to avoid memory overflow
        if (itr + 1) % chunk_size == 0:
            
            # # Convert lists to numpy arrays
            # audio_array = np.array(processed_audio_list)
            # beatmap_array = np.array(processed_beatmap_list)

            # # Save to disk
            # np.save(f'{save_path}/processed_audio_chunk_{itr//chunk_size}.npy', audio_array)
            # np.save(f'{save_path}/processed_beatmap_chunk_{itr//chunk_size}.npy', beatmap_array)
            # Example data

            input_data = [np.array(song) for song in processed_audio_list]
            output_data = [np.array(song) for song in processed_beatmap_list]

            # Create a TensorFlow dataset
            dataset = tf.data.Dataset.from_tensor_slices((input_data, output_data))
            dataset = dataset.batch(1)  # Batch size of 1 for demonstration

            # Custom filename and extension
            filename = f"processed_dataset_{itr//chunk_size}"
            # extension = ".tfdata"  # Custom extension

            # # Define the save path (just the directory part)
            save_path = os.path.join(save_path, filename)

            # Ensure the directory exists
            if not os.path.exists(save_path):
                os.makedirs(save_path)

            # Save the dataset
            tf.data.experimental.save(dataset, save_path)

            # Clear lists to free up memory
            processed_audio_list = []
            processed_beatmap_list = []

        itr+=1
    # Save remaining data
    if processed_audio_list and processed_beatmap_list:
        
        # audio_array = np.array(processed_audio_list)
        # beatmap_array = np.array(processed_beatmap_list)
        # np.save(f'{save_path}/processed_audio_chunk_final.npy', audio_array)
        # np.save(f'{save_path}/processed_beatmap_chunk_final.npy', beatmap_array)

        # input_data = [np.array(song) for song in processed_audio_list]
        # output_data = [np.array(song) for song in processed_beatmap_list]

        # # Create a TensorFlow dataset
        # dataset = tf.data.Dataset.from_tensor_slices((input_data, output_data))
        # dataset = dataset.batch(1)  # Batch size of 1 for demonstration

        # # Custom filename and extension
        # filename = f"processed_beatmap_chunk_final.npy"
        # # extension = ".tfdata"  # Custom extension

        # # # Define the save path (just the directory part)
        # save_path = os.path.join(save_path, filename)

        # # Ensure the directory exists
        # if not os.path.exists(save_path):
        #     os.makedirs(save_path)

        # # Save the dataset
        # tf.data.experimental.save(dataset, save_path)

        # Generator function
    
        # Create dataset
        dataset = create_dataset(processed_audio_list, processed_beatmap_list)

        # Optionally, batch the dataset if needed
        dataset = dataset.batch(1)

        return dataset,itr,processed_audio_list,processed_beatmap_list

    