import sys
import os
import pygame
import html
import ssl
from datetime import datetime
from classifier import *
from downloader import *
from pydub.playback import play
from PIL import Image, ImageDraw, ImageFont

#ch1 bubbling
#ch2 music
#ch3 dj

#get windows desktop path
desktop = os.path.join(os.path.join(os.environ['USERPROFILE']), 'OneDrive')\
.replace("\\","/")+ "/Desktop"
#desktop = os.path.join(os.path.join(os.environ['USERPROFILE']), 'Desktop')\
#.replace("\\","/")

ssl._create_default_https_context = ssl._create_unverified_context

def get_show_names():
    file = open('WKSLG_DJ.txt').readlines()
    file = [line for line in file if ',' in line]
    show_names = {int(line.split(',')[0]): line.split(', ')[-1][:-2] + ' with ' \
                 + line.split('(')[1].split(',')[0] for line in file}
    return show_names

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
        if not artist in song or artist == 'CBSRMT ':
            return_list.append(song)
    return return_list

def visuals_updater(video_info_string):
    try:
        file_string = \
        "<html>\n"\
        +"  <head>\n"\
        +"    <style>\n"\
        +"      body{\n"\
        +"        background-image: url('utils/gifs/AnnMargret_hot_dance_with_Elvis_Presley_in_Viva_Las_Vegas_4.gif');\n"\
        +"        background-size:100%;\n"\
        +"        background-attachment: fixed;\n"\
        +"        height:100%;\n"\
        +"        width:100%;\n"\
        +"        background-position: center;\n"\
        +"        filter: blur(2px);\n"\
        +"        backdrop-filter: blur(1px);\n"\
        +"      }\n"\
        +"    </style>\n"\
        +"    <link href=\"http://fonts.cdnfonts.com/css/kabel\" rel=\"stylesheet\">\n"\
        +"    <script type=\"text/javascript\">\n"\
        +"      const listOfGifs = <listOfGifs>;\n"\
        +"      function run(){\n"\
        +"        var fileName = \"\";\n"\
        +"        fileName = listOfGifs[Math.floor(Math.random()*listOfGifs.length)];\n"\
        +"        document.body.style.backgroundImage = \"url('utils/gifs/\"+fileName+\"')\";\n"\
        +"        window.setTimeout(function(){ document.location.reload(true); }, 15000);\n"\
        +"        //setTimeout(run,15000)\n"\
        +"        //document.getElementById(\"target\").innerHTML = \"ran\";\n"\
        +"        //document.body.style.backgroundImage = \"url('utils/gifs/AnnMargret_hot_dance_with_Elvis_Presley_in_Viva_Las_Vegas_4 (1).gif')\";\n"\
        +"      }\n"\
        +"    </script>\n"\
        +"  </head>\n"\
        +"  <body onload=\"run()\" style=\"background-color:Black;\">\n"\
        +"    <p id=\"target\" style=\"text-shadow: -4px 4px black; font-family: 'Kabel', sans-serif; font-size:25; color:white;position: fixed; bottom: 0; text-align: left\">"\
        +video_info_string\
        +"</p>\n"\
        +"  </body>\n"\
        +"</html>"
        file_string = file_string.replace('<listOfGifs>',str(os.listdir(desktop+'/wkslg/utils/gifs/')))
        file_string = file_string.replace('dj-song<br>','')
        out_file = open(desktop+'/wkslg/visuals.html','w', encoding = 'utf-8')
        out_file.write(file_string)
        out_file.close()
    except:
        visuals_updater("Artist - Unkown, Song - Unknown<br>Mystery Spooky Hour")

def christmasCheck(song_name):
    if datetime.now().month == 12:
        return False
    elif'christmas' in song_name.lower() or 'jingle bell' in song_name.lower()\
        or 'silent night' in song_name.lower() or 'santa' in song_name.lower():
            return True
    else:
        return False
    

def show_starter(show,channels,recovery):
    ch1, ch2, ch3, ch4 = channels
    show_names = get_show_names()
    #getting the folder name
    for folder_name in os.listdir('utils/connectors'):
        if '_' in folder_name:
            if str((show-1)%84) == folder_name.split('_')[0]:
                folder = folder_name
    #getting closer if recovering
    if not recovery:
        closer = pygame.mixer.Sound('utils/connectors/'+folder+'/opener/closer.mp3')
    else:
        all_shows_sounds_file_names = os.listdir('utils/connectors/all_shows_sounds/')
        file_name = random.choice(all_shows_sounds_file_names)
        closer = pygame.mixer.Sound('utils/connectors/all_shows_sounds/'+file_name)
    #playing closer
    visuals_updater(show_names[(show-1)%84])
    start_closer_time = time.time()
    ch3.play(closer,fade_ms=1000)
    fade_in(ch3)
    fade_out(ch1)
    #finding folder name for next show
    for folder_name in os.listdir('utils/connectors'):
        if '_' in folder_name:
            if str(show) == folder_name.split('_')[0]:
                folder = folder_name
    #waiting for closer to finish
    end_time =  max([closer.get_length()+start_closer_time-5,time.time()])
    audible_sound = True
    volume_samples = 20*[1.0]
    while time.time() < end_time and audible_sound:
        if time.time() - start_closer_time > 3:
            for n in range(10):
                volume = ch3.get_volume()
                volume_samples = volume_samples[1:] + [volume]
                time.sleep(0.1)
            if sum(volume_samples)/20 < 0.1:
                audible_sound = False
        else:
            time.sleep(1)
    fade_out(ch3)
    #playing next show opener
    visuals_updater(show_names[show])
    #getting opener if recovering
    if not recovery:
        opener = pygame.mixer.Sound('utils/connectors/'+folder+'/opener/opener.mp3')
    else:
        dj_file_names = os.listdir('utils/connectors/'+folder+'/dj/')
        file_name = random.choice(dj_file_names)
        opener = pygame.mixer.Sound('utils/connectors/'+folder+'/dj/'+file_name)
    start_opener_time = time.time()
    ch3.play(opener,fade_ms=1000)
    fade_in(ch3)
    fade_out(ch1)
    #getting next closer length
    next_closer = pygame.mixer.Sound('utils/connectors/'+folder+'/opener/closer.mp3')
    end_file_length = next_closer.get_length()
    #get songs for next show
    songs = get_songs_for_genre(show,1000)
    bulk_songs = get_songs_for_genre(show,2000,0)
    #find first song
    song_number = random.randint(0,len(songs)-1)
    song_name = songs.pop(song_number)
    artist = song_name.split('-')[0]
    #checking views of first song, block print stops youtube_dl from printing warnings
    block_print()
    song_views, artist_views = 0,0 #get_views(song_name.split('-')[0],song_name.split('-')[1])
    enable_print()
    songs = song_remover(song_name.split('-')[0],songs)
    #getting a new song if the views are too high
    while song_views > 2*10**4 or artist_views > 10**6 \
    or christmasCheck(song_name) and artist != 'CBSRMT ':
        song_number = random.randint(0,len(songs)-1)
        song_name = songs.pop(song_number)
        block_print()
        song_views, artist_views = 0, 0 #get_views(song_name.split('-')[0],song_name.split('-')[1])
        enable_print()
        songs = song_remover(song_name.split('-')[0],songs)
        bulk_songs = song_remover(song_name.split('-')[0],bulk_songs)
    #waiting for opener to finish
    end_time =  max([opener.get_length()+start_opener_time-5,time.time()])
    audible_sound = True
    volume_samples = 20*[1.0]
    while time.time() < end_time and audible_sound:
        if time.time() - start_opener_time > 3:
            for n in range(10):
                volume = ch3.get_volume()
                volume_samples = volume_samples[1:] + [volume]
                time.sleep(0.1)
            if sum(volume_samples)/20 < 0.1:
                audible_sound = False
        else:
            time.sleep(1)
    #turning up the bubbles
    fade_out(ch3)
    fade_in(ch1)
    return songs, bulk_songs, end_file_length, song_name

def show_dj(show,channels):
    ch1, ch2, ch3, ch4 = channels
    try:
        for folder_name in os.listdir('utils/connectors'):
            if '_' in folder_name:
                if str(show) == folder_name.split('_')[0]:
                    folder = folder_name
        connector_file_names = os.listdir('utils/connectors/'+folder+'/sounds/')
        dj_file_names = os.listdir('utils/connectors/'+folder+'/dj/')
        all_shows_file_names = os.listdir('utils/connectors/all_shows/')
        all_shows_file_names.remove('technical_difficulties.mp3')
        all_shows_sounds_file_names = os.listdir('utils/connectors/all_shows_sounds/')
        if random.random() < min([len(connector_file_names)/60,0.5]):
            file_name = random.choice(connector_file_names)
            sound = pygame.mixer.Sound('utils/connectors/'+folder+'/sounds/'+file_name)
            fade_out(ch1)
            ch3.play(sound)
            fade_in(ch3)
            time.sleep(max([sound.get_length()-4,0]))
        elif random.random() < min([len(dj_file_names)/30,0.5]) :
            for folder_name in os.listdir('utils/connectors'):
                if '_' in folder_name:
                    if str(show) == folder_name.split('_')[0]:
                        folder = folder_name
            file_name = random.choice(dj_file_names)
            sound = pygame.mixer.Sound('utils/connectors/'+folder+'/dj/'+file_name)
            fade_out(ch1)
            ch3.play(sound)
            fade_in(ch3)
            time.sleep(max([sound.get_length()-4,0]))
        elif random.random() < min([len(all_shows_file_names)/120,0.5]):
            file_name = random.choice(all_shows_file_names)
            sound = pygame.mixer.Sound('utils/connectors/all_shows/'+file_name)
            fade_out(ch1)
            ch3.play(sound)
            fade_in(ch3)
            time.sleep(max([sound.get_length()-4,0]))
        elif random.random() < min([len(all_shows_file_names)/120,0.5]):
            file_name = random.choice(all_shows_sounds_file_names)
            sound = pygame.mixer.Sound('utils/connectors/all_shows_sounds/'+file_name)
            fade_out(ch1)
            ch3.play(sound)
            fade_in(ch3)
            time.sleep(max([sound.get_length()-4,0]))
    except:
        pass
    fade_out(ch3)
    fade_in(ch1)

def next_shows(artist):
    try:
        #getting the artist page from songkick
        search_artist = artist.replace(' ','+').lower()
        req = urllib.request.Request('https://www.songkick.com/search?page=1&per_page=10&query='\
        +search_artist+'&type=upcoming', headers={'User-Agent': 'Mozilla/5.0'})
        file = urllib.request.urlopen(req).read().decode('utf-8')
        #scraping page for next shows
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
        #getting the artist page from discogs
        search_artist = artist.replace(' ','+').lower()
        req = urllib.request.Request(\
        'https://www.discogs.com/search/?q='+search_artist+'&type=artist'\
        , headers={'User-Agent': 'Mozilla/5.0'})
        file = urllib.request.urlopen(req).read().decode('utf-8')
        url = 'https://www.discogs.com'\
        +file.split('"search_result_title"')[0].split('"')[-2]
        req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
        file = urllib.request.urlopen(req).read().decode('utf-8')
        #scraping for social links
        urls = file.split('"sameAs": [\n  ')[1].split('\n ]')[0][1:-1]
        urls = urls.replace('"','').replace('\n',' '+'\n')
        return artist+"Links:\n\n  "+urls
    except:
        return ""

def shows(channels,show = -1,recovery=False):
    ch1, ch2, ch3, ch4 = channels
    show_names = get_show_names()
    bubbling = pygame.mixer.Sound('utils/background/Bubbling.mp3')
    old_show = -1
    end_file_length = 0
    ch1.play(bubbling, loops=-1)
    fade_in(ch1)
    try:
        while True:
            #try:
            #getting the current hour of the week
            hour = ((time.time()+end_file_length)%604800//3600-79)%168
            #setting the show off of the current hour if it is in the correct time slot
            if (show+1)%84 == int(hour//2) or show == -1:
                show = int(hour//2)
            #checking to start a new show 
            if old_show != show:
                if old_show == -1:
                    songs, bulk_songs, end_file_length, song_name \
                    = show_starter(show, channels, recovery)
                    recovery = False
                    songs_left = True
                else:
                    return show
            old_show = show
            song = pygame.mixer.Sound('library/rotation/'+song_name)
            #set volume
            start_song_time = time.time()
            ch2.play(song,fade_ms=1000)
            fade_in(ch2)
            #printing show name, song, artist, next shows, social links
            #print('\n'+' '*30,show_names[show],'\n'+' '*30,html.unescape(song_name[:-4]))
            video_info_string = html.unescape(song_name[:-4])+'<br>'+show_names[show]
            print(video_info_string)
            visuals_updater(video_info_string)
            band_socials_string = 30*' ' + get_artist_social(song_name.split('-')[0])
            next_shows_string = 30*' ' + next_shows(song_name.split('-')[0])
            '''if len(next_shows_string)>0 and len(band_socials_string) == 0:
                print('\n',html.unescape(next_shows_string).replace('\n','\n'+30*' '))
            elif len(next_shows_string)==0 and len(band_socials_string)>0:
                print('\n',band_socials_string.replace('\n','\n'+30*' '),'\n\n')
            elif len(next_shows_string)>0 and len(band_socials_string)>0:
                print('\n',band_socials_string.replace('\n','\n'+30*' '),'\n\n'\
                ,html.unescape(next_shows_string).replace('\n','\n'+30*' '))
            '''
            #turning off bubbles
            fade_out(ch1)
            #getting the next song.
            if random.random() > 0.2 and len(songs)>0:
                song_number = random.randint(0,len(songs)-1)
                song_name = songs.pop(song_number)
            elif len(bulk_songs)>0:
                song_number = random.randint(0,len(bulk_songs)-1)
                song_name = bulk_songs.pop(song_number)
            elif len(bulk_songs) == 0 and len(songs) == 0:
                show = (show+1)%84
                songs_left = False
                song_name = 'Minor Threat - Filler'
            #getting views
            block_print()
            song_views, artist_views = 0, 0 #get_views(song_name.split('-')[0],song_name.split('-')[1])
            enable_print()
            #removing just played artist
            songs = song_remover(song_name.split('-')[0],songs)
            bulk_songs = song_remover(song_name.split('-')[0],bulk_songs)
            while (song_views > 2*10**4 or artist_views > 10**6) or christmasCheck(song_name) \
            and songs_left:
                if random.random() > 0.2 and len(songs)>0:
                    song_number = random.randint(0,len(songs)-1)
                    song_name = songs.pop(song_number)
                elif len(bulk_songs)>0:
                    song_number = random.randint(0,len(bulk_songs)-1)
                    song_name = bulk_songs.pop(song_number)
                elif len(bulk_songs) == 0 and len(songs) == 0:
                    show = (show+1)%84
                    songs_left = False
                    song_name = 'Minor Threat - Filler'
                block_print()
                song_views, artist_views = 0, 0 #get_views(song_name.split('-')[0],song_name.split('-')[1])
                enable_print()
                #removing just played artist
                songs = song_remover(song_name.split('-')[0],songs)
                bulk_songs = song_remover(song_name.split('-')[0],bulk_songs)
            #waiting for song to finish and checking for dead air
            end_time =  max([song.get_length()+start_song_time-5,time.time()])
            audible_sound = True
            volume_samples = 20*[1.0]
            while time.time() < end_time and audible_sound:
                if time.time() - start_song_time > 3:
                    for n in range(10):
                        volume = ch2.get_volume()
                        volume_samples = volume_samples[1:] + [volume]
                        time.sleep(0.1)
                else:
                    time.sleep(1)
                if sum(volume_samples)/20 < 0.1:
                    audible_sound = False
            fade_in(ch1)
            ch2.fadeout(10**3)
            show_dj(show, channels)
    except:
        return show