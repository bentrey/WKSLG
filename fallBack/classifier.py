import librosa
import os
import langdetect
import urllib.request
import time
import pandas as pd
import numpy as np
from googlesearch import search
from tqdm.notebook import tqdm
#from sklearn.neural_network import MLPClassifier
#from sklearn.ensemble import RandomForestClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.preprocessing import MultiLabelBinarizer
from sklearn.model_selection import train_test_split


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
        'cs11v', 'cs12v', 'label','genre']
        df = pd.DataFrame(columns=columns)
    else:
        df =  pd.read_csv('songs.csv')
    directory = 'library/'
    w = os.walk(directory)
    folders = next(w)[1]
    for folder in tqdm(folders,desc="Folders",leave=False):
        songs = os.listdir(directory+folder)
        for song_name in tqdm(songs,desc="Songs",leave=False):
            if not song_name in list(df['name']):
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
                new_row.append('[]')
                df.loc[df.index.max()+1] = new_row
                df.to_csv('songs.csv',index=False)    
                
def remove_missing():
    w = os.walk('library/')
    files = []
    new_files = next(w,False)
    while new_files:
        files.extend(new_files[2])
        new_files = next(w,False)
    df = pd.read_csv('songs.csv')
    df = df[df['name'].isin(files)]
    df.to_csv('songs.csv',index=False)
    
def get_pickles():
    pass

def get_genres(rewrite=False,google=False):
    df = pd.read_csv('songs.csv')
    artists = list(df['name'])
    empties = df['genre'] == '[]'
    for n in tqdm(range(len(artists)),desc="songs",leave=False):
        try:
            if '-' in artists[n]:
                artists[n] = ' '.join(artists[n].split('-')[:-1])
            if artists[n][-1] == ' ':
                artists[n] = artists[n][:-1]
            if empties[n] or rewrite:
                url = 'https://www.last.fm/music/'+artists[n].replace(' ','+')
                if google:
                    urls = list(search(artists[n]+' last.fm'))
                    url = urls[0]
                    time.sleep(58+30*np.random.rand())
                    for temp_url in urls:
                        if 'last.fm' in temp_url and not 'last.fm' in url:
                            url = temp_url
                file = urllib.request.urlopen(url).read().decode("utf-8")
                if 'class="catalogue-tags' in file:
                    tags = file.split('class="catalogue-tags "')[1].split("</ul>")[0].replace(' ','')
                    tags_list = tags.split("/tag/")[1:]
                if len(tags_list)>1:
                    for m in range(len(tags_list)):
                        tags_list[m] = tags_list[m].split('"')[0]
                df.iat[n,70] = str(tags_list)
                df.to_csv('songs.csv',index=False) 
        except Exception as e:
            print(artists[n])
            print(e)

def get_songs_for_genre(label,number_of_songs,alpha=0.05):
    #opening songs.cvs, giving label to songs in two locations
    df = pd.read_csv('safesongs.csv')
    songs = []
    for folder in os.listdir('library'):
        if str(label) == folder.split('_')[0]:
            songs = os.listdir('library/'+folder)
            df_duplicates = df[df['name'].isin(songs)].copy()
            df_duplicates['label'] = label
            df = pd.concat([df,df_duplicates]).drop_duplicates().reset_index(drop=True)
    #finding genres in training data
    folder_df = df[df['label']>=0]
    genre_labels = []
    for index,row in folder_df.iterrows():
        genre_list = row['genre'][2:-2].split("', '")
        for genre in genre_list:
            if not genre in genre_labels:
                genre_labels.append(genre)
    #vectorizing data
    df = df[['name','label','genre']]
    df['genre'] = df.genre.apply(lambda x: x[2:-2].split("', '"))
    mlb = MultiLabelBinarizer(sparse_output=True)
    df = df.join(
        pd.DataFrame.sparse.from_spmatrix(
        mlb.fit_transform(df.pop('genre')),
        index=df.index,
        columns=mlb.classes_))
    #training
    df['bool_label'] = df.label.apply(lambda x: x==label)
    drops = []
    for column in df.columns:
        if not column in genre_labels+['label','bool_label','name']:
            drops.append(column)
    df = df.drop(drops,axis=1)
    df_training = df[df['label']>=0].drop('label',axis=1)
    df_rotation = df[df['label']<0].drop('label',axis=1)
    y = df_training['bool_label']
    X = df_training.drop(['bool_label','name'],axis=1)
    keep_going = True
    while keep_going:
        try:
            lr = LogisticRegression()
            lr.fit(X,y)
            keep_going = False
        except:
            pass
    probabilities = lr.predict_proba(df_rotation.drop(['name','bool_label'],1))
    maxes = probabilities[:,1].copy()
    maxes.sort()
    df_rotation = df_rotation[probabilities[:,1] >= max([maxes[-number_of_songs],alpha])]
    #df_rotation = df_rotation[probabilities[:,1] > maxes[-number_of_songs]]
    return list(df_rotation['name'])

def get_songs_for_genre_kmeans(label):
    #opening songs.cvs, giving label to songs in two locations
    df = pd.read_csv('safesongs.csv')
    songs = []
    for folder in os.listdir('library'):
        if str(label) == folder.split('_')[0]:
            songs = os.listdir('library/'+folder)
            df_duplicates = df[df['name'].isin(songs)].copy()
            df_duplicates['label'] = label
            df = pd.concat([df,df_duplicates]).drop_duplicates().reset_index(drop=True)
    #finding genres in training data
    folder_df = df[df['label']==-1]
    genre_labels = []
    for index,row in folder_df.iterrows():
        genre_list = row['genre'][2:-2].split("', '")
        for genre in genre_list:
            if not genre in genre_labels:
                genre_labels.append(genre)
    #getting final columns
    df_training = df[df['label']==-1]
    df_training = df_training[['name','label','genre']]
    df_training['genre'] = df_training.genre.apply(lambda x: x[2:-2].split("', '"))
    mlb = MultiLabelBinarizer(sparse_output=True)
    df_training = df_training.join(
        pd.DataFrame.sparse.from_spmatrix(
        mlb.fit_transform(df_training.pop('genre')),
        index=df_training.index,
        columns=mlb.classes_))
    #vectorizing data
    df = df[['name','label','genre']]
    df['genre'] = df.genre.apply(lambda x: x[2:-2].split("', '"))
    mlb = MultiLabelBinarizer(sparse_output=True)
    df = df.join(
        pd.DataFrame.sparse.from_spmatrix(
        mlb.fit_transform(df.pop('genre')),
        index=df.index,
        columns=mlb.classes_))
    df = df[df.columns.intersection(list(df_training.columns))]
    #training
    y = df['name']
    X = df.drop(['name','label'],axis=1)
    keep_going = True
    while keep_going:
        try:
            kmeans = KMeans(n_clusters=20, random_state=0).fit(X)
            keep_going = False
        except:
            pass
    df['kmeans'] = kmeans.labels_
    genre_songs = get_songs_for_genre(label,500)
    label_value = df[df['name'].isin(genre_songs)]['kmeans'].value_counts().idxmax()
    df = df[df['kmeans']==label_value]
    return list(df['name'])

def get_songs_for_genre_2(label,number_of_songs):
    df = pd.read_csv('safesongs.csv')
    for folder in os.listdir('D:/library'):
        if str(label) == folder.split('_')[0]:
            print(label)
            songs = os.listdir('D:/library/'+folder)
            df_duplicates = df[df['name'].isin(songs)].copy()
            df_duplicates['label'] = label
            df = pd.concat([df,df_duplicates]).drop_duplicates().reset_index(drop=True)
    df_training = df[df['label'] == label]
    print(df_training['label'].value_counts())
    genres_dictionary = {}
    for index,row in df_training.iterrows():
        genres = row['genre'][2:-2].split("', '")
        for genre in genres:
            genres_dictionary[genre] = genres_dictionary.get(genre,0) + 1
    df_rotation = df[df['label'] < 0]
    df_rotation = df_rotation[['name','genre']]
    df_rotation['score'] \
        = df_rotation.genre.apply(lambda x: sum([genres_dictionary.get(y,0) for y in x[2:-2].split("', '")]))
    scores = list(df_rotation['score'])
    scores.sort()
    df_rotation = df_rotation[df_rotation['score'] > scores[-number_of_songs]]
    return list(df_rotation['name'])