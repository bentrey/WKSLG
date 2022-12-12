import sys
import os
import pygame
import html
import ssl
from datetime import datetime
from classifier import *
from downloader import *
from pydub.playback import play
import random
# from show_dev import *

# SLUDGE_LIBRARY = os.listdir(path="/Volumes/WKSLG/WKSLG/library") # the USB
pygame.mixer.init()
ch1 = pygame.mixer.Channel(0)
ch2 = pygame.mixer.Channel(1)
ch3 = pygame.mixer.Channel(2)
ch4 = pygame.mixer.Channel(3)

LOCAL = os.getcwd() # gets current directory of WKSLG folder

class Show:
    '''
    Show is an instance of ONE single show, includes openers/closers
    as well as a list of songs that will be played during this instances
    hour (the method in which it gets songs may result in different songs
    each time it is run though)
    '''
    def __init__(self, show):
        self.show = show
        self.start = True # if True, play the opener , if false don't
        self.folder = None
        self.opener = None
        self.closer = None
        self.dj = None
        self.sounds = None
        self.songs = None

    def initialize(self, num_songs):
        # populate opener, closer, folder, and song list
        try:
            self.folder = self._set_folder()
            self.opener = self._set_opener()
            self.closer = self._set_closer()
            self.dj_files = self._set_dj()
            self.sounds = self._set_sounds()
            self.songs = get_songs_for_genre(self.show, num_songs) # integet value is # songs to return from function
        except Exception as e:
            # some better error handling....
            print("Error initializing show:", e)
            return False # in sludge.py check if this returns false and handle it there

    # def start_show(self):
    #     # starts the show, plays opener
    #     # original file plays the closer for the previous show
    #         # but I'll try just the starter for now
    #     opener_time = time.time()
    #     ch3.play(self.opener, fade_ms=1000)
    #     fade_in(ch3)
    #     fade_out(ch1) # holdover from playing closer

    #     # get next closer length? 
    #         # self.closer
    #         # end_file_length = self.closer.get_length() get_length is pygame Sound method
    #     # songs vs bulk songs
    #     song_number = random.randint(0, len(self.songs) - 1)
    #     song_name = self.songs.pop(song_number)
    #     artist = song_name.split('-')[0]
    #     # print("SONG AND ARTIST", song_name, artist)

    #     end_time = max([self.opener.get_length() + opener_time - 5, time.time()])
    #     audible_sound = True
    #     volume_samples = 20*[1.0]
    #     while time.time() < end_time and audible_sound:
    #         if time.time() - opener_time > 3:
    #             for n in range(10):
    #                 volume = ch3.get_volume()
    #                 volume_samples = volume_samples[1:] + [volume]
    #                 time.sleep(0.1)
    #             if sum(volume_samples)/20 < 0.1:
    #                 audible_sound = False
    #         else:
    #             time.sleep(1)
    #     fade_out(ch3)
    #     fade_in(ch1)

    def get_show(self):
        return self.show

    def toggle_show_start_off(self):
        # after the start of show, turn off self.show_start
        self.start = False

    def _set_folder(self):
        # get the folder for the show
        folder = None
        try:
            # for folder_name in os.listdir('./utils/connectors'): # use standard path os.listdir instead
            for folder_name in os.listdir(f'{LOCAL}/library'):
                if "_" in folder_name:
                    if folder_name == 'DS Store': # DS_Store is macOS thing 
                        continue
                if str((self.show)) == folder_name.split('_')[0]:
                    folder = folder_name
        except Exception as e:
            # use some default error folder?
            print("Error folder in setter", e)

        return folder

    def _set_closer(self):
        # get the closer for the show as a pygame Sound object
        # assumes pygame mixer has been loaded already(same for opener)
        return pygame.mixer.Sound(f'{LOCAL}/utils/connectors/{self.folder}/opener/closer.mp3')
        # return pygame.mixer.Sound(f'./utils/connectors/{self.folder}/opener/closer.mp3')

    def _set_opener(self):
        # sets the opener for the show as a pygame Sound object
        return pygame.mixer.Sound(f'{LOCAL}/utils/connectors/{self.folder}/opener/opener.mp3')
        # return pygame.mixer.Sound(f'./utils/connectors/{self.folder}/opener/opener.mp3')

    def _set_dj(self): # possibly 'play' dj and not just 'get'
        # Get the dj files to play
        dj_files = os.listdir(f"{LOCAL}/utils/connectors/{self.folder}/dj")
        # dj_files = os.listdir(f"./utils/connectors/{self.folder}/dj")
        return dj_files

    def _set_sounds(self):
        # get all sounds associated with show
        sounds = os.listdir(f"{LOCAL}/utils/connectors/{self.folder}/sounds")
        # sounds = os.listdir(f"./utils/connectors/{self.folder}/sounds")
        return sounds


    def choose_song(self):
        # from the songs, select a song, randomly, remove it from the list, and return it to be played
        '''
        WIll choose the song from the actual file location where the song is stored
        For now return a random song and print it

        '''

        random_number = random.randint(0, len(self.songs) - 1) 
        song = self.songs.pop(random_number) # will return this song whilst removing the song from the list
        return song

    def get_songs(self):
        '''
        returns the list of songs
        '''
        return self.songs
    
    def print_songs_info(self):
        # display the song and artist info when playing a song
        for song in self.songs:
            print(song)

    def __str__(self):
        # return 'none'
        return f"SHOW: {self.folder, self.songs, self.show}"
    

def play_file(file):
    # play file for testing
    print("FILE:", file)
    start_time = time.time()
    ch3.play(file, fade_ms = 1000)
    fade_in(ch3)
    fade_out(ch1)

    end_time = max([file.get_length() + start_time - 5, time.time()])
    audible_sound = True
    volume_samples = 20 * [1.0]
    while time.time() < end_time and audible_sound:
        if time.time() - start_time > 3:
            for n in range(10):
                volume = ch3.get_volume()
                volume_samples = volume_samples[1:] + [volume]
                time.sleep(0.1)
            if sum(volume_samples) / 20 < 0.1:
                audible_sound = False
        else:
            time.sleep(1)
    fade_out(ch3)

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

# test = Show(62)
# test.initialize()
# # test.choose_song()
# test.start()
# test.print_songs()
# time.sleep(1000)
# play_file(test.opener)
# play_file(test.opener)

# test = Show(12)
# test.initialize(3)
