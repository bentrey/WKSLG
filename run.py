import os
import sys
import datetime
import time
import pygame
import random
import show
from importlib import reload
from pydub.playback import play
import warnings

warnings.filterwarnings("ignore")

sys.stdout = open(os.devnull, 'w')
pygame.mixer.init()
sys.stdout = sys.__stdout__
ch1 = pygame.mixer.Channel(0)
ch2 = pygame.mixer.Channel(1)
ch3 = pygame.mixer.Channel(2)
ch4 = pygame.mixer.Channel(3)

'''def run():
    global ch1, ch2, ch3, ch4
    bubbling = pygame.mixer.Sound('D:/utils/background/Bubbling.mp3')
    old_show = -1
    ch1.play(bubbling, loops=-1)
    fade_in(ch1)
    while True:
        try:
            hour = (time.time()%604800//3600-79)%168
            show = hour//2
            if old_show != show:
                songs = show_starter(show)
            old_show = show
            #print(songs)
            song_number = random.randint(0,len(songs)-1)
            song_name = songs.pop(song_number)
            print(show,song_name)
            song = pygame.mixer.Sound('D:/library/rotation/'+song_name)
            #ch2.play(song)
            ch2.play(song,fade_ms=1000)
            fade_out(ch1)
            #sleep time
            ###############volume setter
            ##############replace below with while loop checking volume
            time.sleep(song.get_length()-5)
            #time.sleep(10)
            fade_in(ch1)
            ch2.fadeout(10**3)
            show_dj(show)
        except:
            pygame.mixer.init()
            ch1 = pygame.mixer.Channel(0)
            ch2 = pygame.mixer.Channel(1)
            ch3 = pygame.mixer.Channel(2)
            ch4 = pygame.mixer.Channel(3)
            end_of_world \
            = pygame.mixer.Sound('D:/utils/connectors/all_shows/technical_difficulties.mp3')
            ch1.play(end_of_world)
            time.sleep(end_of_world.get_length()-5)
            run()'''

def run(recover=False):
    global ch1, ch2, ch3, ch4
    channels = [ch1, ch2, ch3, ch4]
    while True:
        reload(show)
        #try:
        show.shows(channels)
        '''except:
            pygame.mixer.init()
            ch1 = pygame.mixer.Channel(0)
            ch2 = pygame.mixer.Channel(1)
            ch3 = pygame.mixer.Channel(2)
            ch4 = pygame.mixer.Channel(3)
            end_of_world \
            = pygame.mixer.Sound('/utils/connectors/all_shows/technical_difficulties.mp3')
            ch1.play(end_of_world)
            channels = [ch1, ch2, ch3, ch4]
            time.sleep(end_of_world.get_length()-5)
            run(channels, recovery=True)'''

run()
