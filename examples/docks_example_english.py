# -*- coding: utf-8 -*-
"""
Created on Wed Aug  2 14:16:35 2017

@author: twiefel
"""
import os
import sys
sys.path.append("../../")
from docks.docks import suppress_alsa_warnings
from docks.docks.sentencelist_postprocessor import SentencelistPostprocessor
import speech_recognition as sr
from pprint import pprint

if __name__ == "__main__":
    os.system('tput reset')
    terminal_name = 'DOCKS EXAMPLE'
    sys.stdout.write("\x1b]2;"+terminal_name+"\x07")
    

    english_sentence_list = "./pizzeria.sentences.txt"
    language = "english"
    language_code = "en-EN"    
    
    # obtain audio from the microphone
    google_recognizer = sr.Recognizer()
    sentencelist_postprocessor = SentencelistPostprocessor(english_sentence_list,language)

    #adjust microphone to background noise
    with sr.Microphone() as source:
        google_recognizer.adjust_for_ambient_noise(source)

    while True:
        raw_input("PRESS ENTER TO START RECOGNITION")
        with sr.Microphone() as source:
            print("Say something!")
            audio = google_recognizer.listen(source)

            try:
                # for testing purposes, we're just using the default API key
                # to use another API key, use `r.recognize_google(audio, key="GOOGLE_SPEECH_RECOGNITION_API_KEY")`
                # instead of `r.recognize_google(audio)`

                google_hypotheses = google_recognizer.recognize_google(audio, language = language_code)
                print "Google understood:",google_hypotheses
                
                result,confidence = sentencelist_postprocessor.recognize(google_hypotheses)

                print "DOCKS understood: ", result
                print "DOCKS confidence: ",confidence

            except sr.UnknownValueError:
                print("Google Speech Recognition could not understand audio")
            except sr.RequestError as e:
                print("Could not request results from Google Speech Recognition service; {0}".format(e)) 

