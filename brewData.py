#This script calls all functions and process audio and beatmap into processed formatted data and store on disk
from dotenv import load_dotenv
import os
import pandas as pd
from beatmap import *



def brew():
    #select dataset from metadata
    df=pd.read_csv("metadata.csv")
    # df = df[(df["difficultyrating"]>5) & (df["difficultyrating"]<5.0005) & (df["split"]=="train")]
    df = df[df["audio"].str.contains("c367ac169")]

    # Preprocess and store all audio data tobe trained
    from preprocessaudio import preprocess_and_save_audio
    preprocess_and_save_audio(df)


    # Cook the .osu data
    load_osu_files_from_df(df)

    #save metadata also for retrieval later
    save_df_as_numpy(df)
