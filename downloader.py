from googlesearch import search
from spotipy.oauth2 import SpotifyClientCredentials
from youtubesearchpython import VideosSearch
import spotipy
import os
import random
import youtube_dl
import credentials
import time
import pandas as pd
import numpy as np

path = 'library'

def get_file(artist, song, dir="library", max_views=2*10**4):
    index = 0
    term = artist + ' ' + song
    #urls = google_search(term)
    ydl_opts = {'format': 'bestaudio/best', 'postprocessors': [{'key': 'FFmpegExtractAudio',\
        'preferredcodec': 'mp3', 'preferredquality': '192',}],'noplaylist':True, \
        'outtmpl': path + '/'+artist+' - '+song+'.%(ext)s', 'quite':True,}
    with youtube_dl.YoutubeDL(ydl_opts) as ydl:
        entries = ydl.extract_info(f"ytsearch:{artist} {song}", download=False)
        total_views = 0
        for n in range(len(entries['entries'])):
            total_views += entries['entries'][n]['view_count']
        url = entries['entries'][0]['webpage_url']
        if total_views<max_views:
            ydl.extract_info(url)
        else:
            print('Too many views')

def get_views(artist, song, dir="library"):
    try:
        index = 0
        term = artist + ' ' + song
        #urls = google_search(term)
        ydl_opts = {'quite':True, 'no_warnings':True, 'format': 'bestaudio/best', 'postprocessors': \
                   [{'key': 'FFmpegExtractAudio', 'preferredcodec': 'mp3', 'preferredquality'\
                   : '192',}],'noplaylist':True, 'outtmpl': path + '/'+artist+' - '+song+'.%(ext)s',\
                   'ignoreerrors':True, 'cookies':'youtube.com_cookies.txt'}
        with youtube_dl.YoutubeDL(ydl_opts) as ydl:
            entries = ydl.extract_info(f"ytsearch:{artist} {song}", download=False)
            song_total_views = 0
            for n in range(len(entries['entries'])):
                song_total_views += entries['entries'][n]['view_count']
            entries = ydl.extract_info(f"ytsearch:{artist}", download=False)
            artist_total_views = 0
            for n in range(len(entries['entries'])):
                artist_total_views += entries['entries'][n]['view_count']
        return song_total_views, artist_total_views
    except:
        return 10**9, 10**9

def google_search(terms):
    time.sleep(58+30*np.random.rand())
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

def wfmu_downloader(times,includes=None, max_views=2*10**4, back=0):
    wfmu_playlists = os.listdir('wfmu_html')
    if back != 0:
        wfmu_playlists.sort()
        wfmu_playlists = wfmu_playlists[-back:]
    for n in range(times):
        file_name = random.choice(wfmu_playlists)
        print(file_name)
        file = open('wfmu_html/'+file_name,errors='replace').read()
        if includes != None:
            while not includes in file:
                file_name = random.choice(wfmu_playlists)
                print(file_name)
                file = open('wfmu_html/'+file_name).read()
        df = ''
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
                elif 'the stooge' in columns:
                    df = test_df
        files = np.array(os.listdir('library/rotation'))
        if len(df)>0:
            df = df.fillna(method='ffill')
            for n in range(df.shape[0]):
                try:
                    row = df.iloc[n]
                    artist = row[df.columns[0]]
                    song = row[df.columns[1]]
                    print(artist,song)
                    #artist_tracks = np.flatnonzero(np.core.defchararray.find(files,artist)!=-1)
                    #song_tracks = np.flatnonzero(np.core.defchararray.find(files,song)!=-1)
                    #same_song_locations = np.intersect1d(artist_tracks, song_tracks)
                    #if len(same_song_locations) == 0 and (len(artist)+len(song))<100:
                    get_file(artist, song, max_views=max_views)
                except:
                    print('get_file() failed')

def spotify_playlist_downloader(playlist_id, max_views=2*10**4):
    n=0
    cid = credentials.cid
    secret = credentials.secret
    client_credentials_manager = SpotifyClientCredentials(client_id=cid, client_secret=secret)
    spotify = spotipy.Spotify(client_credentials_manager = client_credentials_manager)
    results = spotify.playlist(playlist_id, fields="tracks,next")
    downloads = []
    tracks = results['tracks']
    while tracks:
        for item in tracks['items']:
            artist = (item['track']['artists'][0]['name'])
            track = (item['track']['name'])
            downloads.append((artist,track))
        tracks = spotify.next(tracks)
    for download in downloads:
        artist, track = download
        try:
            print(artist,track,n)
            n += 1
            get_file(artist,track,max_views=max_views)
        except:
            print('get_file failed')

def spotify_album_downloader(album_id, max_views=2*10**4):
    cid = credentials.cid
    secret = credentials.secret
    client_credentials_manager = SpotifyClientCredentials(client_id=cid, client_secret=secret)
    spotify = spotipy.Spotify(client_credentials_manager = client_credentials_manager)
    results = spotify.album(album_id)
    for n in range(len(results['tracks']['items'])):
        artist = results['artists'][0]['name']
        track = results['tracks']['items'][n]['name']
        print(artist,track)
        try:
            get_file(artist,track,max_views=max_views) 
        except:
            print('get_file failed')

def library_downloader(trials):
    w = os.walk('/library/')
    files = os.listdir('/library/rotation/')
    cid = credentials.cid
    secret = credentials.secret
    client_credentials_manager = SpotifyClientCredentials(client_id=cid, client_secret=secret)
    spotify = spotipy.Spotify(client_credentials_manager = client_credentials_manager)
    for trial in range(trials):
        try:
            keep_going = True
            index = [0]
            while keep_going:
                artist = '-'.join(random.choice(files).split('-')[:-1])
                if sum([int(artist in name) for name in files])<5:
                    items = spotify.search(artist,type='playlist')['playlists']['items']
                    if len(items)>0:
                        for n in range(len(items)):
                            if items[n]['name'].lower() == 'this is '+artist.lower():
                                keep_going = False
                                index = n
                        for n in range(len(items)):
                            if items[n]['name'].lower() == artist.lower()+' radio':
                                keep_going = False
                                index = n
            #id = items[random.randint(0,len(items))]['id']
            id = items[n]['id']
            spotify_playlist_downloader(id)
        except:
            time.sleep(100)

def youtube_downloader(numberOfSongs, dir="library"):
    for n in range(numberOfSongs):
        try:
            title = np.random.choice(os.listdir('library/rotation/'))
            artist = title.split("-")[0]
            videosSearch = VideosSearch(artist, limit = 10)
            choice = np.random.choice(videosSearch.result()['result'])
            title = choice['title']
            duration = choice['duration']
            times = duration.split(':')
            if len(times) == 2:
                if int(times[0]) < 20:
                    artist = title.split("-")[0]
                    song = "-".join(title.split("-"))
                    get_file(artist, song)
            elif len(times) == 1:
                artist = title.split("-")[0]
                song = "-".join(title.split("-"))
                get_file(artist, song)
        except:
            pass

def spotify_crawler(n):
    files = os.listdir(path + '/rotation')
    temp_files = []
    for file in files:
        if not (file.split('-')[0].lower(), True) in temp_files:
            temp_files.append((file.split('-')[0].lower(), True))
        else :
            temp_files.append((file.split('-')[0].lower(), False))
    files = []
    for file in temp_files:
        if file[1]:
            files.append(file[0])
    cid = credentials.cid
    secret = credentials.secret
    client_credentials_manager = SpotifyClientCredentials(client_id=cid, client_secret=secret)
    spotify = spotipy.Spotify(client_credentials_manager = client_credentials_manager)
    for n in range(n):
        try:
            artist = np.random.choice(files)
            artist_string = spotify.search(artist)['tracks']['items'][0]['artists'][0]['external_urls']['spotify'].split('/')[-1]
            artist_uri = 'spotify:artist:'+artist_string
            results = spotify.artist_albums(artist_uri, album_type='album')
            album_string = results['items'][0]['external_urls']['spotify'].split('/')[-1]
            print(artist)
            spotify_album_downloader(album_string)
        except:
            pass