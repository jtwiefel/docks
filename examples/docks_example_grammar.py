# -*- coding: utf-8 -*-
"""
Created on Wed Oct 24 16:38:12 2018

@author: twiefel
"""

import os
import sys
sys.path.append("../../")
from docks.docks import suppress_alsa_warnings
import speech_recognition as sr
from pprint import pprint

if __name__ == "__main__":
    os.system('tput reset')
    terminal_name = 'DOCKS EXAMPLE'
    sys.stdout.write("\x1b]2;"+terminal_name+"\x07")
    

    english_jsgf_grammar = "./icecream.gram"


    new_lm_folder = "./icecream"
    #generate grammar files
    from docks.docks import grammar_generation
    grammar_generation.generate_grammar_language_model(jsgf_grammar_file = english_jsgf_grammar, 
                                                   new_lm_folder = new_lm_folder)
    
    from docks.docks.grammar_postprocessor import GrammarPostprocessor
    grammar_postprocessor = GrammarPostprocessor(lm_folder_path = new_lm_folder)
    
    #grammar initializiation is non blocking so wait some time
    import time
    time.sleep(5)
    


    # obtain audio from the microphone
    google_recognizer = sr.Recognizer()

    #adjust the microphone to background noise
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

                google_hypotheses = google_recognizer.recognize_google(audio)
                print "Google understood:",google_hypotheses
                
                result = grammar_postprocessor.recognize(google_hypotheses)
                print "DOCKS understood: ", result

            except sr.UnknownValueError:
                print("Google Speech Recognition could not understand audio")
            except sr.RequestError as e:
                print("Could not request results from Google Speech Recognition service; {0}".format(e)) 