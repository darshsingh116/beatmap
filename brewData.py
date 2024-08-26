#This script calls all functions and process audio and beatmap into processed formatted data and store on disk
from dotenv import load_dotenv
import os
import pandas as pd
from beatmap import *
from preprocessaudio import preprocess_and_save_audio,preprocess_and_save_audio_in_parallel
import time



def brew():

    #note time for audio
    tic = time.time()

    #select dataset from metadata
    df=pd.read_csv("metadata.csv")
    df = df[(df["difficultyrating"]>5) & (df["difficultyrating"]<5.001) & (df["split"]=="train")]
    #df = df[df["audio"].str.contains("c367ac169")]

    # Preprocess and store all audio data tobe trained
    
    preprocess_and_save_audio_in_parallel(df)
    # preprocess_and_save_audio(df)

    # End the timer (Toc)
    toc = time.time()

    # Calculate and print the elapsed time
    elapsed_time = toc - tic
    print(f"Elapsed time to preprocess audio: {elapsed_time:.2f} seconds")


    #note time for beatmap
    tic = time.time()

    # Cook the .osu data
    load_osu_files_from_df(df)

    #save metadata also for retrieval later
    save_df_as_numpy(df)


     # End the timer (Toc)
    toc = time.time()

    # Calculate and print the elapsed time
    elapsed_time = toc - tic
    print(f"Elapsed time to preprocess beatmaps: {elapsed_time:.2f} seconds")