from googlesearch import search
import os
import random
import youtube_dl

path = 'library'
ydl_opts = {'format': 'bestaudio/best', 'noplaylist':True, 'outtmpl': path + '/%(title)s.%(ext)s',}

def get_file(term, dir="/library"):
    index = 0
    urls = google_search(term)
    with youtube_dl.YoutubeDL(ydl_opts) as ydl:
        while index < len(urls):
            url = urls[index]
            if 'youtube.com' in url:
                entry = ydl.extract_info(url, download=False)
                title = entry['title']
                if title_tester(title):
                    entries = ydl.extract_info(url)
                    index = len(urls)
            index += 1

def google_search(terms):
    return list(search(terms, stop=10))

def title_tester(title):
    okay = True
    print('title', title)
    if 'official' in str(title).lower():
        okay = False
    return okay

def wfmu_downloader():
    wfmu_playlists = os.listdir('wfmu_html')
    for n in range(1):
        file_name = random.choice(wfmu_playlists)
        print('file_name')
        file = open('wfmu_html/'+file_name).read()
        tables = file.split('<table')
        playlist_table = ''
        for table in tables:
            artist_in = "Artist" in table
            track_in = "Track" in table
            if artist_in and track_in:
                playlist_table = '<table'+table.split('</table>')[0]+'</table>'
        if playlist_table != '':
            df = pd.read_html(playlist_table)[0]
            for n in df.shape[0]:
                row = df.iloc[n]
                print(row['Artist'], row['Track'])
                get_file(row['Artist']+' '+row['Track'])
wfmu_downloader()