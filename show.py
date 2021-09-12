import sys
import os
import pygame
import html
from classifier import *
from downloader import *
from pydub.playback import play

#ch1 bubbling
#ch2 music
#ch3 dj

file = open('WKSLG_DJ.txt').readlines()
file = [line for line in file if ',' in line]
show_names = {int(line.split(',')[0]): line.split(', ')[-1][:-2] + ' with ' \
             + line.split('(')[1].split(',')[0] for line in file}

def block_print():
    sys.stdout = open(os.devnull, 'w')

def enable_print():
    sys.stdout = sys.__stdout__

def fade_in(sound):
    while sound.get_volume()<0.99:
        sound.set_volume(sound.get_volume()+0.1)
        time.sleep(0.3)

def fade_out(sound):
    while sound.get_volume()>0.1:
        sound.set_volume(sound.get_volume()-0.1)
        time.sleep(0.3)

def song_remover(artist,songs):
    return_list = []
    for song in songs:
        if not artist in song:
            return_list.append(song)
    return return_list

def show_starter(show,channels,recovery):
    ch1, ch2, ch3, ch4 = channels
    for folder_name in os.listdir('/utils/connectors'):
        if '_' in folder_name:
            if str((show-1)%84) == folder_name.split('_')[0]:
                folder = folder_name
    if  not recovery:
        starter = pygame.mixer.Sound('/utils/connectors/'+folder+'/opener/closer.mp3')
    else: 
        file = random.choice(os.listdir('/utils/connectors/'+folder+'/dj/'))
        starter = pygame.mixer.Sound('/utils/connectors/'+folder+'/dj/'+file)
    ch3.play(starter,fade_ms=1000)
    fade_out(ch1)
    time.sleep(max([starter.get_length()-5,0]))
    fade_in(ch1)
    for folder_name in os.listdir('/utils/connectors'):
        if '_' in folder_name:
            if str(show) == folder_name.split('_')[0]:
                folder = folder_name
    opener = pygame.mixer.Sound('/utils/connectors/'+folder+'/opener/opener.mp3')
    ch3.play(opener,fade_ms=1000)
    song_start_time = time.time()
    next_closer = pygame.mixer.Sound('/utils/connectors/'+folder+'/opener/closer.mp3')
    end_file_length = next_closer.get_length()
    fade_out(ch1)
    songs = get_songs_for_genre(show,1000)
    bulk_songs = get_songs_for_genre(show,2000,0)
    song_number = random.randint(0,len(songs)-1)
    song_name = songs.pop(song_number)
    block_print()
    song_views, artist_views = get_views(song_name.split('-')[0],song_name.split('-')[1])
    enable_print()
    songs = song_remover(song_name.split('-')[0],songs)
    while song_views > 2*10**4 or artist_views > 10**6:
        song_number = random.randint(0,len(songs)-1)
        song_name = songs.pop(song_number)
        block_print()
        song_views, artist_views = get_views(song_name.split('-')[0],song_name.split('-')[1])
        enable_print()
        songs = song_remover(song_name.split('-')[0],songs)
        bulk_songs = song_remover(song_name.split('-')[0],bulk_songs)
    time.sleep(max([opener.get_length()-5+time.time()-song_start_time,0]))
    fade_in(ch1)
    return songs, bulk_songs, end_file_length, song_name

def show_dj(show,channels):
    ch1, ch2, ch3, ch4 = channels
    try:
        event = random.random()
        if event < 0.3:
            for folder_name in os.listdir('/utils/connectors'):
                if '_' in folder_name:
                    if str(show) == folder_name.split('_')[0]:
                        folder = folder_name
            file_names = os.listdir('/utils/connectors/'+folder+'/sounds/')
            if len(file_names)>0:
                file_name = random.choice(file_names)
                sound = pygame.mixer.Sound('/utils/connectors/'+folder+'/sounds/'+file_name)
                fade_out(ch1)
                ch3.play(sound)
                time.sleep(max([sound.get_length()-2,0]))
                fade_in(ch1)
        elif event<0.4:
            for folder_name in os.listdir('/utils/connectors'):
                if '_' in folder_name:
                    if str(show) == folder_name.split('_')[0]:
                        folder = folder_name
            file_names = os.listdir('/utils/connectors/'+folder+'/dj/')
            if len(file_names)>0:
                file_name = random.choice(file_names)
                sound = pygame.mixer.Sound('/utils/connectors/'+folder+'/dj/'+file_name)
                fade_out(ch1)
                ch3.play(sound)
                time.sleep(max([sound.get_length()-2,0]))
                fade_in(ch1)
        elif event<0.5:
            file_names = os.listdir('/utils/connectors/all_shows/')
            file_names.remove('technical_difficulties.mp3')
            if len(file_names)>0:
                file_name = random.choice(file_names)
                sound = pygame.mixer.Sound('/utils/connectors/all_shows/'+file_name)
                fade_out(ch1)
                ch3.play(sound)
                time.sleep(max([sound.get_length()-2,0]))
                fade_in(ch1)
    except:
        pass
    fade_in(ch1)

def next_shows(artist):
    try:
        search_artist = artist.replace(' ','+').lower()
        file = urllib.request.urlopen(\
        'https://www.songkick.com/search?page=1&per_page=10&query='+search_artist+'&type=upcoming')\
        .read().decode('utf-8')
        if 'sorry' in file.lower():
            return ''
        else:
            return_string = 'Upcoming Events featuring '+artist+'\n\n'
            for n in range(1,min([file.count('<time'),3])+1):
                event = '  '+file.split('<p class="summary">')[n].split('<strong>')[1]\
                .split('</strong>')[0]
                if len(event)>24:
                    event = event[:20] + ' ...'
                location = '  '+file.split('<p class="location">')[n].split('</p>')[0].strip()\
                .replace('\n','')
                date = '  '+file.split('<time')[n].split('>')[1].split('<')[0]
                return_string = return_string+event+'\n'+location+'\n'+date+'\n\n'
        return return_string
    except:
        return ''

def get_artist_social(artist):
    try:
        search_artist = artist.replace(' ','+').lower()
        req = urllib.request.Request(\
        'https://www.discogs.com/search/?q='+search_artist+'&type=artist'\
        , headers={'User-Agent': 'Mozilla/5.0'})
        file = urllib.request.urlopen(req).read().decode('utf-8')
        url = 'https://www.discogs.com'\
        +file.split('"search_result_title"')[0].split('"')[-2]
        req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
        file = urllib.request.urlopen(req).read().decode('utf-8')
        urls = file.split('"sameAs": [\n  ')[1].split('\n ]')[0][1:-1].replace('"','')
        return artist+" Links:\n\n  "+urls
    except:
        return ""

def shows(channels,recovery=False):
    ch1, ch2, ch3, ch4 = channels
    bubbling = pygame.mixer.Sound('/utils/background/Bubbling.mp3')
    old_show = -1
    show = -1
    end_file_length = 0
    ch1.play(bubbling, loops=-1)
    fade_in(ch1)
    while True:
        try:
            hour = ((time.time()+end_file_length)%604800//3600-79)%168
            if (show+1)%84 == int(hour//2) or show == -1:
                show = int(hour//2)
            if old_show != show:
                songs, bulk_songs, end_file_length, song_name = show_starter(show, channels, recovery)
                recovery = False
                songs_left = True
            old_show = show
            song = pygame.mixer.Sound('/library/rotation/'+song_name)
            #set volume
            ch2.play(song,fade_ms=1000)
            print('\n',show_names[show],'\n',html.unescape(song_name[:-4]))
            band_socials_string = get_artist_social(song_name.split('-')[0])
            next_shows_string = next_shows(song_name.split('-')[0])
            if len(next_shows_string)>0 and len(band_socials_string) == 0:
                print('\n',html.unescape(next_shows_string))
            elif len(next_shows_string)==0 and len(band_socials_string)>0:
                print('\n',band_socials_string,'\n\n')
            elif len(next_shows_string)>0 and len(band_socials_string)>0:
                print('\n',band_socials_string,'\n\n',html.unescape(next_shows_string))
            fade_out(ch1)
            start_song_time = time.time()
            if random.random() > 0.2 and len(songs)>0:
                song_number = random.randint(0,len(songs)-1)
                song_name = songs.pop(song_number)
            elif len(bulk_songs)>0:
                song_number = random.randint(0,len(bulk_songs)-1)
                song_name = bulk_songs.pop(song_number)
            elif len(bulk_songs) == 0 and len(songs) == 0:
                show = (show+1)%84
                songs_left = False
            block_print()
            song_views, artist_views = get_views(song_name.split('-')[0],song_name.split('-')[1])
            enable_print()
            songs = song_remover(song_name.split('-')[0],songs)
            bulk_songs = song_remover(song_name.split('-')[0],bulk_songs)
            while (song_views > 2*10**4 or artist_views > 10**6) and songs_left:
                if random.random() > 0.2 and len(songs)>0:
                    song_number = random.randint(0,len(songs)-1)
                    song_name = songs.pop(song_number)
                elif len(bulk_songs)>0:
                    song_number = random.randint(0,len(bulk_songs)-1)
                    song_name = bulk_songs.pop(song_number)
                elif len(bulk_songs) == 0 and len(songs) == 0:
                    show = (show+1)%84
                    songs_left = False
                block_print()
                song_views, artist_views = get_views(song_name.split('-')[0],song_name.split('-')[1])
                enable_print()
                songs = song_remover(song_name.split('-')[0],songs)
                bulk_songs = song_remover(song_name.split('-')[0],bulk_songs)
            time.sleep(max([song.get_length()-time.time()+start_song_time-5,0]))
            fade_in(ch1)
            ch2.fadeout(10**3)
            show_dj(show, channels)
        except Exception as e:
            print(e)
            if 'songname' in locals():
                print(songname)