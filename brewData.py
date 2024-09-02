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
    df = df[(df["mode"] == 0) & (df["difficultyrating"]>4.8) & (df["difficultyrating"]< 6) & (df["split"]=="train")]
    # df = df[df["audio"]=="0013ddfd8bd55fdccc0b253e313b7a60"]
    # df = df[df["audio"]=="21f85de72bd9ab9338b7f68252bf848f"]
    df = df[0:1000]

    # Preprocess and store all audio data tobe trained
    
    # preprocess_and_save_audio_in_parallel(df)
    # preprocess_and_save_audio(df)

    # End the timer (Toc)
    toc = time.time()

    # Calculate and print the elapsed time
    elapsed_time = toc - tic
    print(f"Elapsed time to preprocess audio: {elapsed_time:.2f} seconds")


    # #note time for beatmap
    tic = time.time()

    # Cook the .osu data
    load_osu_files_from_df(df)

    #we are saving metadata inside load_osu_siles_from_df func as we are modifying df with addition of hyperparams and then saving


     # End the timer (Toc)
    toc = time.time()

    # Calculate and print the elapsed time
    elapsed_time = toc - tic
    print(f"Elapsed time to preprocess beatmaps: {elapsed_time:.2f} seconds")