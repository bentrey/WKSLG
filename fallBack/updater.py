import librosa
import os
import langdetect
import urllib.request
import time
import spotipy
import pandas as pd
import numpy as np
import credentials
from googlesearch import search
from tqdm import tqdm
from spotipy.oauth2 import SpotifyClientCredentials
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
    for folder in tqdm(folders,desc="Classifier: Folders",leave=False):
        songs = os.listdir(directory+folder)
        for song_name in tqdm(songs,desc="Classifier: Songs",leave=False):
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

def get_genres(rewrite=False,google=False,spotify=False):
    cid = credentials.cid
    secret = credentials.secret
    client_credentials_manager = SpotifyClientCredentials(client_id=cid, client_secret=secret)
    spotify = spotipy.Spotify(client_credentials_manager = client_credentials_manager)
    df = pd.read_csv('songs.csv')
    artists = list(df['name'])
    empties = df['genre'] == '[]'
    for n in tqdm(empties[empties].index,desc="Genre: Songs",leave=False):
        try:
            if '-' in artists[n]:
                artists[n] = ' '.join(artists[n].split('-')[:-1])
            if artists[n][-1] == ' ':
                artists[n] = artists[n][:-1]
            old_tags = df[df['name'].str.contains(artists[n])]
            old_tags = old_tags[old_tags['genre'] != '[]']
            if len(old_tags) > 0:
                tags_list = list(old_tags['genre'])[0]
                df.iat[n,70] = tags_list
                empties[n] = False
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
                elif spotify:
                    artist = spotify.search(q="artist : "+artists[n],type="artist")['artists']['items']
                    if len(artist)>0:
                        tags_list = artist[0]["genre"]
                    else:
                        tags_list="[]"
                df.iat[n,70] = str(tags_list)
                df.to_csv('songs.csv',index=False) 
        except Exception as e:
            print(artists[n])
            print(e)

def get_songs_for_genre(label,number_of_songs):
    df = pd.read_csv('songs.csv')
    df = df[['label','genre']]
    df['genre'] = df.genre.apply(lambda x: x[2:-2].split("', '"))
    mlb = MultiLabelBinarizer(sparse_output=True)
    df = df.join(
        pd.DataFrame.sparse.from_spmatrix(
        mlb.fit_transform(df.pop('genre')),
        index=df.index,
        columns=mlb.classes_))
    df = df[df['label']>0]
    df['label'] = df.label.apply(lambda x: x==label)
    y = df['label']
    X = df.drop('label',axis=1)
    lr = LogisticRegression()
    lr.fit(X,y)  
    df = pd.read_csv('D:/songs.csv')
    df = df[['name','label','genre']]
    df['genre'] = df.genre.apply(lambda x: x[2:-2].split("', '"))
    mlb = MultiLabelBinarizer(sparse_output=True)
    df = df.join(
        pd.DataFrame.sparse.from_spmatrix(
        mlb.fit_transform(df.pop('genre')),
        index=df.index,
        columns=mlb.classes_))
    df = df[df['label']<0]
    probabilities = lr.predict_proba(df.drop(['name','label'],1))
    maxes = probabilities[:,1].copy()
    maxes.sort()
    df = df[probabilities[:,1] > maxes[-number_of_songs]]
    return list(df['name'])

def get_songs_for_genre(label):
    #opening songs.cvs, giving label to songs in two locations
    df = pd.read_csv('songs.csv')
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

remove_missing()
classifier()
get_genres(spotify=True)
get_genres(google=True)