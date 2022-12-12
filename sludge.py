'''
Actual radio object, that handles all the running of the show

eg sludge = Sludge(recover=False)
sludge.run()
'''
from ast import Break
import os
import sys
import datetime
import time
import pygame
import random
import show_dev # importing this will run the show_dev.py file
import warnings
from importlib import reload
from pydub.playback import play
from show_obj import Show
from downloader import get_file, get_views, spotify_playlist_downloader
import threading as th
pygame.mixer.init()

LOCAL = os.getcwd() # current path directory of WKSLG folder
try:
    # if sludge volume is connected, get path, else return false
    SLUDGE_LIBRARY = os.listdir(path="/Volumes/WKSLG/WKSLG/library")
except:
    SLUDGE_LIBRARY = False
# make 4 channels
# ch1 bubbling
# ch2 music
# ch3 dj/connectors
ch1 = pygame.mixer.Channel(0)
ch2 = pygame.mixer.Channel(1)
ch3 = pygame.mixer.Channel(2)
ch4 = pygame.mixer.Channel(3)

class Sludge:
    '''
    Assumes all the pygame stuff has already initialized
    But maybe load it all here, who knows.
    '''
    def __init__(self, recovery):
        # self.run = False
        self.recovery = recovery
        self.shows = None # this will be ALL the shows
        self.show = None # keep this as the integer value of the show
            # however if it is the object, then it can persist
            # with any persistent attributes of the object
            # on each loop of run()

    def initialize(self):
        # do set up, get show, set sounds, etc.
        self.show = Show(self.get_show()[0]) # don't necessarily instantiate a new show, but check if its a new show
        self.show.initialize(10)

    def get_show(self):
        '''
        return the current show based on current time.
        '''
        old_show = -1
        show = -1
        end_file_length = 0
        hour = ((time.time() + end_file_length) % 604800 // 2600-79) % 168
        if (show + 1) % 84 == int(hour//2) or show == -1:
            show = int(hour//2)
        return show, old_show

    def get_from_internet(self, file_name):
        # get the file from youtube if it isn't found in storage

        '''
        view check, if fails, return False, if successful move one and 
        download file
        '''

        # print(song_name.split())
        artist = True
        artist_name = []
        song_name = []
        for word in file_name.split():
            if word == "-":
                artist = False
                continue
            if artist == True:
                artist_name.append(word)
            elif artist == False:
                song_name.append(word)
        
        full_artist_name = " ".join(artist_name)
        full_song_name = " ".join(song_name).split('.mp3')[:-1][0]

        try:
            get_file(full_artist_name, full_song_name)
            return True
        except Exception as e:
            print("Error:", e)
            return False
    
    def get_artist_song_names(self, filename):
        # return artist and song name as strings from the string fill name
        artist = True
        artist_name = []
        song_name = []
        for word in filename.split():
            if word == "-":
                artist = False
                continue
            if artist == True:
                artist_name.append(word)
            elif artist == False:
                song_name.append(word)
        
        full_artist_name = " ".join(artist_name)
        full_song_name = " ".join(song_name).split('.mp3')[:-1][0]
        return full_artist_name, full_song_name

    def view_check(self, max_views, filename):
        # returns False if too many views on youtube
        # get views checks youtube for video data, will return a bunch of "downloading webpage"
            # type stuff
        artist, song = self.get_artist_song_names(filename)
        artist_views, song_views = get_views(artist, song)
        if song_views > max_views:
            print("Too many views", artist, song)
            # too many views, return false
            return False




    def _return_failsafe(self):
        '''Returns a random song from the show folder as a failsafe
        '''
        random_num = random.randint(0, len(os.listdir(LOCAL + f"/library/{self.show.folder}")) - 1)

        for index, song in enumerate(os.listdir(LOCAL + f"/library/{self.show.folder}")):
            if index == random_num:
                print("RETUNRING FAILSAFE", song)
                return pygame.mixer.Sound(LOCAL + f"/library/{self.show.folder}/{song}")
                    
    def _choose_song(self, show, test=False):
        # handles song selection and playback
        # show is the Show Object
        # test = True will load songs from the local directory instead of main sludge directory
        song = None
        while song == None:
            try:
                song_name = ''
                # counter = 0
                # # while self.view_check(2 * 10 ** 4, show.choose_song()) == False:
                # while True:
                #     counter += 1
                #     song_name = show.choose_song()
                #     if self.view_check(2 * 10 ** 4, song_name) == False:
                #         continue
                #     if counter > 2:
                #         print("No song found that matches view count requirement")
                #         return False
                song_name = show.choose_song() # this is a song that is chose from the CSV
                # print(self.show, song_name)
                # return False
                # song_name = "Tales Under the Oak - Peculiar Shapes.mp3"
                # self.get_from_internet(song_name)
                if test == True:
                    # if True get a song form local directory just to play
                    self._return_failsafe()
                    # random_num = random.randint(0, len(os.listdir(LOCAL + f"/library/{self.show.folder}")) - 1)

                    # for index, song in enumerate(os.listdir(LOCAL + f"/library/{self.show.folder}")):
                    #     if index == random_num:
                    #         return pygame.mixer.Sound(LOCAL + f"/library/{self.show.folder}/{song}")
                    
                else:
                    # get the file itself, and return that
                    # else, return the song from song name

                    for file in  os.listdir(LOCAL + f"/library/rotation"):
                        if file == song_name:
                            return pygame.mixer.Sound(LOCAL + f"/library/rotation/{file}")
                    # Need a way to download song if not found 
                    # If song is not returned in loop, play failsafe song, but download song in background
                    try:
                        
                        failsafe = self._return_failsafe()
                        play_failsafe = th.Thread(target=self.play_file, args=[failsafe])
                        download_file = th.Thread(target=self.get_from_internet, args=[song_name]) # need some loop to make sure that the song passes view check
                        # create a loop and wait for these two threads to finish BEFORE moving on
                        play_failsafe.start()
                        download_file.start()
                        play_failsafe.join()
                        download_file.join()
     
                        print("Playing song: ", song_name)
                        return pygame.mixer.Sound(LOCAL + f"/library/rotation/{song_name}")
                    except Exception as e:
                        print("Could not get song", e)
                        continue

                
                    # print("Folder not found", self.get_from_internet(song_name))
                    return False
            except:
                # return some sound file if song not found
                # if song not found, play some fail safe song/commercial/sound while downloading the file in the
                # background, when files finishes downloading, play the file

                print("Song not found", song)
                break
        return song


    def _new_show_check(self):
        # check the time and see if it is a new show
        return self.show.show != self.get_show()[0] # if true, not new show, if false, new show

    def show_start(self):
        # handle show initialization
        # and play the opener?
        self.show.initialize()

    def play_file(self, file, bubbling=False):
        '''
        handles the playing of a file, including
        getting the file length, loading it into the pygame mixer
        setting up all the channel fade in/out,waiting until the file as finished playing 
        '''
        play_song = pygame.mixer.Sound(file)

        opener_time = time.time()
        ch3.play(play_song, fade_ms=1000)
        fade_in(ch3)
        fade_out(ch1) # holdover from playing closer?

        if bubbling == True:
            # 
            end_time = max([play_song.get_length() + opener_time - 5, time.time()]) // 28
        else:
            end_time = max([play_song.get_length() + opener_time - 5, time.time()])
        audible_sound = True
        volume_samples = 20*[1.0]
        while time.time() < end_time and audible_sound:
            if time.time() - opener_time > 3:
                for n in range(10):
                    volume = ch3.get_volume()
                    volume_samples = volume_samples[1:] + [volume]
                    time.sleep(0.1)
                if sum(volume_samples)/20 < 0.1:
                    audible_sound = False
            else:
                time.sleep(1)
        fade_out(ch3)
        fade_in(ch1)

    def play_bubbling(self):
        self.play_file(LOCAL + f"/utils/background/Bubbling.mp3", bubbling=True)

    def run(self):
        # the sludge must flow

        self.initialize() # initial sludge setup, setups up show for current hour
        self.show.toggle_show_start_off() # comment out to run from opener
        
        # print(self.show.get_songs())

        while True:
            # main loop, check for new show on each loop, otherwise keep
            # check if new show
            if self._new_show_check() == True:
                # return False
                self.initialize()

            # if not new show, keep current show
            try:
                if self.show.start == True:
                    # play opener
                    self.play_file(self.show.opener)
                    self.show.toggle_show_start_off()
                    continue

                # play bubbling between songs
                self.play_bubbling()
                # song = self._choose_song(self.show) # comment out for test vice versa
                song = self._choose_song(self.show, False) # True here tells it to choose from local library folders
                print("Song chosen and playing", song)
                self.play_file(song) 
            except Exception as e:
                # if error play end of times or backwards song
                # or choose from the current show folder
                print("Error in new loop", e)
                self.play_bubbling()
                song = self._choose_song(self.show, True)
                print(self.show, song)
                self.play_file(song)

def fade_in(sound):
    '''
    'fades in' sound
    '''
    while sound.get_volume() < 0.99:
        sound.set_volume(sound.get_volume() + 0.1)
        time.sleep(0.3)

def fade_out(sound):
    '''
    'fades out' sound
    '''
    while sound.get_volume() > 0.1:
        sound.set_volume(sound.get_volume() - 0.1)
        time.sleep(0.3)


sludge = Sludge(False)

sludge.run()

    

def get_from_internet(file_name):
    # get the file from youtube if it isn't found in storage


    # print(song_name.split())
    artist = True
    artist_name = []
    song_name = []
    for word in file_name.split():
        if word == "-":
            artist = False
            continue
        if artist == True:
            artist_name.append(word)
        elif artist == False:
            song_name.append(word)
    
    full_artist_name = " ".join(artist_name)
    full_song_name = " ".join(song_name).split('.mp3')[:-1][0]
    get_file(full_artist_name, full_song_name)
    # return " ".join(artist_name), " ".join(song_name).split('.mp3')[:-1][0]

# get_from_internet("Tales Under the Oak - Peculiar Shapes.mp3")
# print(get_from_internet("Black Flag - Nervous Breakdown.mp3"))
# artist, song = get_from_internet("Black Flag - Nervouse Breakdown.mp3")
# get_file(artist, song, dir="./test_library")
# spotify_playlist_downloader("1PTQyZZAm4IWb5iVvTkBPu?si=5f006bfa257d4ba7")
