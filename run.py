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

#get windows desktop path
desktop = os.path.join(os.path.join(os.environ['USERPROFILE']), 'OneDrive')\
.replace("\\","/")+ "/Desktop"
#desktop = os.path.join(os.path.join(os.environ['USERPROFILE']), 'Desktop')\
#.replace("\\","/")


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
    show_id = int((((time.time())%604800//3600-79)%168)//2)
    print('\n'*50)
    #this for loop will run for each show
    while True:
        try:
            #reloads show.py
            reload(show)
        except Exception as e:
            print(e)
        try:
            #runs the current show, using the shows function in show.py
            show_id = show.shows(channels, show=show_id,recovery=recovery)
        except Exception as e:
            print(e)
            try:
                #this runs if an error occured in show.shows
                #restarts pygame mixer
                pygame.mixer.init()
                #makes new channels
                ch1 = pygame.mixer.Channel(0)
                ch2 = pygame.mixer.Channel(1)
                ch3 = pygame.mixer.Channel(2)
                ch4 = pygame.mixer.Channel(3)
                ch1.set_volume(0)
                #playing bubbles
                bubbles = pygame.mixer.Sound(desktop+'/wkslg/background.wav')
                ch1.play(bubbles)
                show.fade_in(ch1)
                #getting backwards opener
                clip = random.choice(os.listdir(desktop+'/wkslg/backwards/opener'))
                opener \
                = pygame.mixer.Sound(desktop + '/wkslg/backwards/opener/' + clip)
                #playing backwards song
                ch3.play(opener)
                time.sleep(opener.get_length())
                show.fade_out(ch1)
                #getting backwards song
                song = random.choice(os.listdir(desktop+'/wkslg/backwards'))
                print(desktop + '/' + song)
                backwards \
                = pygame.mixer.Sound(desktop + '/wkslg/backwards/' + song)
                #updating visuals
                file = open(desktop+'/wkslg/visuals_template.html', 'r')
                file_string = file.read()
                file_string = file_string.replace('artist-song<br>dj-show',song.replace(".mp3",""))
                file.close()
                file = open(desktop+'/wkslg/visuals.html','w')
                file.write(file_string.encode('utf-8'))
                file.close()
                #playing backwards song
                ch2.play(backwards)
                channels = [ch1, ch2, ch3, ch4]
                #waiting 
                time.sleep(backwards.get_length())
                run(recovery=True)
            except:
                try:
                    #this runs if an error occured in show.shows
                    #restarts pygame mixer
                    pygame.mixer.init()
                    #makes new channels
                    ch1 = pygame.mixer.Channel(0)
                    ch2 = pygame.mixer.Channel(1)
                    ch3 = pygame.mixer.Channel(2)
                    ch4 = pygame.mixer.Channel(3)
                    time.sleep(10)
                    #getting the end of times message
                    end_of_world \
                    = pygame.mixer.Sound(desktop + '/wkslg/technical_difficulties.mp3')
                    #updating visuals
                    file = open(desktop+'/wkslg/visuals_template.html', 'r')
                    file_string = file.read()
                    file_lines = file_string.split('\n')
                    for n, line in enumerate(file_lines):
                        if "document.body.style.backgroundImage =" in line:
                            file_lines[n] = "document.body.style.backgroundImage = \"url('technical_difficulties.gif')\";"
                    file_string = "\n".join(file_lines)
                    file_string = file_string.replace('artist-song<br>dj-show',"")
                    file.close()
                    file = open(desktop+'/wkslg/visuals.html','w')
                    file.write(file_string.encode('utf-8'))
                    file.close()
                    #playing end of times message
                    ch1.play(end_of_world)
                    channels = [ch1, ch2, ch3, ch4]
                    #waiting 
                    time.sleep(end_of_world.get_length())
                    run(recovery=True)
                except:
                    run(recovery=True)

run()