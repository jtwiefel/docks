# -*- coding: utf-8 -*-
"""
Created on Wed Aug  2 14:16:35 2017

@author: twiefel
"""
import os
import sys
sys.path.append("../../")
from docks.docks import suppress_alsa_warnings
import speech_recognition as sr
from pprint import pprint
from docks.docks.docks import g2p

if __name__ == "__main__":
    os.system('tput reset')
    terminal_name = 'DOCKS EXAMPLE'
    sys.stdout.write("\x1b]2;"+terminal_name+"\x07")
    

    
    # obtain audio from the microphone
    google_recognizer = sr.Recognizer()
    g2p_converter = g2p.GraphemeToPhonemeConverter()

    path = '/home/sysadmin/twiefel/phoneme_experiments/corpus/audio/'
    for idx in range(10):
        filename = path+str(idx)+'.wav'
        with sr.AudioFile(filename) as source:
            audio = google_recognizer.record(source)  # read the entire audio file
            try:
                # for testing purposes, we're just using the default API key
                # to use another API key, use `r.recognize_google(audio, key="GOOGLE_SPEECH_RECOGNITION_API_KEY")`
                # instead of `r.recognize_google(audio)`
                
                		#to get all results use:
                #google_hypotheses = google_recognizer.recognize_google(audio,show_all=True)
                google_hypotheses = google_recognizer.recognize_google(audio)
                #print google_hypotheses
                google_hypotheses = google_hypotheses.encode('ascii','ignore').lower()
                pprint(google_hypotheses)
                print g2p_converter.get_phonemes_for_sentence(google_hypotheses)
     

            except sr.UnknownValueError:
                print("Google Speech Recognition could not understand audio")
            except sr.RequestError as e:
                print("Could not request results from Google Speech Recognition service; {0}".format(e)) 

