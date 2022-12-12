#importing stuff
import os
import sys
import datetime
import time
import pygame
import random
import show
import warnings
from importlib import reload
from pydub.playback import play

#removing warnings from print out
warnings.filterwarnings("ignore")

#starting pygame mixer to play sounds
pygame.mixer.init()
#making 4 channels
#ch1 bubbling
#ch2 music
#ch3 dj/connectors
ch1 = pygame.mixer.Channel(0)
ch2 = pygame.mixer.Channel(1)
ch3 = pygame.mixer.Channel(2)
ch4 = pygame.mixer.Channel(3)

#this function starts radio running
def run(recovery=False):
    #this specifies the channels created outside the function
    global ch1, ch2, ch3, ch4
    channels = [ch1, ch2, ch3, ch4]
    #this for loop will run for each show
    while True:
        #reloads show.py
        reload(show) # checks for new show (show checks time each time it is run,which determines show)
        try:
            print("Try")
            #runs the current show, using the shows function in show.py
            show.shows(channels,recovery)
        except:
            # #this runs if an error occured in show.shows
            # #restarts pygame mixer
            # pygame.mixer.init()
            # #makes new channels
            # ch1 = pygame.mixer.Channel(0)
            # ch2 = pygame.mixer.Channel(1)
            # ch3 = pygame.mixer.Channel(2)
            # ch4 = pygame.mixer.Channel(3)
            # #getting the end of times message
            # # end_of_world = pygame.mixer.Sound('')
            # # = pygame.mixer.Sound('/utils/connectors/all_shows/technical_difficulties.mp3')
            # #playing end of times message
            # ch1.play(end_of_world)
            # channels = [ch1, ch2, ch3, ch4]
            # #waiting 
            # time.sleep(end_of_world.get_length()-5)
            # run(recovery=True)
            print("Not working")
            break

run()
