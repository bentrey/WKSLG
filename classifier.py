import librosa
import os
import langdetect
import pandas as pd
import numpy as np

def classifier(rewrite=False):
    #file name, lang, zero_crossing_rate, spectral_centroid,
    #spectral_rolloff, Mel-Frequency_Cepstral_Coefficients\
    #chroma_frequencies
    if rewrite:
        columns = ['name', 'lang', 'zero_crossings', 'spectral_centroid', \
        'spectral_rolloff', 'mf1m', 'mf2m', 'mf3m', 'mf4m', 'mf5m', \
        'mf6m', 'mf7m', 'mf8m', 'mf9m', 'mf10m', 'mf11m', 'mf12m', \
        'mf13m', 'mf14m', 'mf15m', 'mf16m', 'mf17m', 'mf18m', 'mf19m', \
        'mf20m', 'mf1v', 'mf2v', 'mf3v', 'mf4v', 'mf5v', 'mf6v', 'mf7v', \
        'mf8v', 'mf9v', 'mf10v', 'mf11v', 'mf12v', 'mf13v', 'mf14v', \
        'mf15v', 'mf16v', 'mf17v', 'mf18v', 'mf19v', 'mf20v', 'cs1m', \
        'cs2m', 'cs3m', 'cs4m', 'cs5m', 'cs6m', 'cs7m', 'cs8m', 'cs9m', \
        'cs10m', 'cs11m', 'cs12m', 'cs1v', 'cs2v', 'cs3v', \
        'cs4v', 'cs5v', 'cs6v', 'cs7v', 'cs8v', 'cs9v', 'cs10v', \
        'cs11v', 'cs12v', 'label']
        df = pd.DataFrame(columns=columns)
    else:
        df =  pd.read_csv('D:/songs.csv')
    directory = 'D:/library/'
    w = os.walk(directory)
    folders = next(w)[1]
    for folder in folders:
        songs = os.listdir(directory+folder)
        for song_name in songs:
            if not song_name in list(df['name']):
                print(song_name)
                new_row = []
                new_row.append(song_name)
                new_row.append(langdetect.detect(song_name))
                song, sr = librosa.load(directory+folder+'/'+song_name)
                new_row.append(np.mean(librosa.zero_crossings(song)))
                new_row.append(np.mean(librosa.feature.spectral_centroid(song, sr=sr)[0]))
                new_row.append(np.mean(librosa.feature.spectral_rolloff(song+0.01, sr=sr)[0]))
                new_row = new_row + list(librosa.feature.mfcc(song, sr=sr).mean(axis=1))
                new_row = new_row + list(librosa.feature.mfcc(song, sr=sr).var(axis=1))
                new_row = new_row + list(librosa.feature.chroma_stft(song, sr=sr).mean(axis=1))
                new_row = new_row + list(librosa.feature.chroma_stft(song, sr=sr).var(axis=1))
                if folder == 'rotation':
                    new_row.append(-1)
                else:
                    new_row.append(int(folder.split('_')[0]))
                df.loc[df.index.max()+1] = new_row
    df.to_csv('D:/songs.csv',index=False)