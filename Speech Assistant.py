# -*- coding: utf-8 -*-
"""
Created on Mon Nov  4 22:47:24 2024

@author: Hp
"""

import speech_recognition as sr
import webbrowser
import time
import pygame  # replacing playsound with pygame
import os
import random
from gtts import gTTS
from time import ctime

# Set the full path to the FLAC executable
# os.environ["FLAC"] = r"C:\Users\Hp\Downloads\flac-1.4.3-win\flac-1.4.3-win\Win64"
import sys

# Add FLAC path to system PATH
flac_path = r"C:\Users\Hp\Downloads\flac-1.4.3-win\flac-1.4.3-win\Win64"
os.environ["PATH"] += os.pathsep + flac_path

# Initialize pygame mixer
pygame.mixer.init()

r = sr.Recognizer()

def record_audio(ask=False):
    with sr.Microphone() as source:
        if ask:
            Gerard_speak(ask)
        audio = r.listen(source)
        voice_data = ''
        try:
            voice_data = r.recognize_google(audio)
        except sr.UnknownValueError:
            Gerard_speak('Sorry, I did not get that...')
        except sr.RequestError:
            Gerard_speak('Sorry, my speech service is down!')
    return voice_data

def Gerard_speak(audio_string):
    tts = gTTS(text=audio_string, lang='en')
    r = random.randint(1, 10000000)
    audio_file = f"audio-{r}.mp3"
    tts.save(audio_file)
    
    # Play the audio using pygame
    pygame.mixer.music.load(audio_file)
    pygame.mixer.music.play()
    
    # Wait for the audio to finish playing
    while pygame.mixer.music.get_busy():
        continue
    
    # Unload the music and wait a moment to release the file
    pygame.mixer.music.unload()
    time.sleep(0.1)  # Short delay to ensure file is released

    # Now remove the audio file
    os.remove(audio_file)
    print(audio_string)


def respond(voice_data):
    if 'what is your name' in voice_data:
        Gerard_speak('My name is Gerard Way')
    elif 'what time is it' in voice_data:
        Gerard_speak(ctime())
    elif 'search' in voice_data:  
        search = record_audio('What do you want to search for?')
        url = 'https://google.com/search?q=' + search
        webbrowser.get().open(url)
        Gerard_speak(f'Here is what I found for {search}')
    elif 'find location' in voice_data:  
        location = record_audio('What is the location?')
        url = 'https://google.nl/maps/place/' + location + '/&amp;'
        webbrowser.get().open(url)
        Gerard_speak(f'Here is the location of {location}')
    elif 'exit' in voice_data:
        Gerard_speak("Goodbye!")
        exit()

time.sleep(1)
Gerard_speak('How can I help you?')

while True:
    voice_data = record_audio()
    respond(voice_data)
