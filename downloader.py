from googlesearch import search
from spotipy.oauth2 import SpotifyClientCredentials
import spotipy
import os
import random
import youtube_dl
import pandas as pd
import numpy as np
import credentials

path = 'library'

def get_file(artist, song, dir="/library"):
    index = 0
    term = artist + ' ' + song
    urls = google_search(term)
    ydl_opts = {'format': 'bestaudio/best', 'postprocessors': [{'key': 'FFmpegExtractAudio',\
        'preferredcodec': 'mp3', 'preferredquality': '192',}],'noplaylist':True, \
        'outtmpl': path + '/'+artist+' - '+song+'.%(ext)s',}
    with youtube_dl.YoutubeDL(ydl_opts) as ydl:
        while index < len(urls):
            url = urls[index]
            if 'youtube.com' in url:
                entry = ydl.extract_info(url, download=False)
                title = entry['title']
                if title_tester(title, term):
                    entries = ydl.extract_info(url)
                    index = len(urls)
            index += 1

def google_search(terms):
    return list(search(terms, stop=10))

def title_tester(title, term):
    okay = True
    print('title', title)
    terms = term.split(' ')
    left_over = str(title)
    for term in terms:
        left_over.replace(term, '')
    if 'official' in str(title).lower():
        okay = False
    elif '(live)' in str(title).lower():
        okay = False
    return okay

def wfmu_downloader(includes=None):
    wfmu_playlists = os.listdir('wfmu_html')
    for n in range(10):
        file_name = random.choice(wfmu_playlists)
        print(file_name)
        file = open('wfmu_html/'+file_name).read()
        if includes != None:
            while not includes in file:
                file_name = random.choice(wfmu_playlists)
                print(file_name)
                file = open('wfmu_html/'+file_name).read()
        tables = file.split('<table')
        for n in range(len(tables)):
            tables[n] = '<table'+tables[n].split('</tables>')[0]+'</table>'
        for table in tables:
            test_df = pd.read_html(table)
            if len(test_df)>0:
                test_df = test_df[0]
                columns = [str(col).lower() for col in list(test_df.columns)]
                if 'artist' in columns:
                    df = test_df
        files = np.array(os.listdir('library'))
        if len(df)>0:
            df = df.fillna(method='ffill')
            for n in range(df.shape[0]):
                try:
                    row = df.iloc[n]
                    artist = row[df.columns[0]]
                    song = row[df.columns[1]]
                    print(artist,song)
                    artist_tracks = np.flatnonzero(np.core.defchararray.find(files,artist)!=-1)
                    song_tracks = np.flatnonzero(np.core.defchararray.find(files,song)!=-1)
                    same_song_locations = np.intersect1d(artist_tracks, song_tracks)
                    if len(same_song_locations) == 0:
                        get_file(artist, song)
                except:
                    print('get_file() failed')

def spotify_playlist_downloader(playlist_id):
    cid = credentials.cid
    secret = credentials.secret
    client_credentials_manager = SpotifyClientCredentials(client_id=cid, client_secret=secret)
    spotify = spotipy.Spotify(client_credentials_manager = client_credentials_manager)
    results = spotify.playlist('2OOarnLNBNgkHMbT3rgUCJ')
    for item in results['tracks']['items']:
        artist = (item['track']['artists'][0]['name'])
        track = (item['track']['name'])
        print(artist,track)
        get_file(artist,track)
