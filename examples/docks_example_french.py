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
from docks.docks.sentencelist_postprocessor import SentencelistPostprocessor


def multilingual_asr():
    
    french_sentence_list = "./french.sentences.txt"
    language = "french"
    language_code = "fr-FR"

    sentence_list = french_sentence_list

    
    # obtain audio from the microphone
    google_recognizer = sr.Recognizer()
    sentencelist_postprocessor = SentencelistPostprocessor(sentence_list, language)

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

                google_hypotheses = google_recognizer.recognize_google(audio, language=language_code)
                print "Google understood:",google_hypotheses
                
                result,confidence = sentencelist_postprocessor.recognize(google_hypotheses)

                print "DOCKS understood: ", result
                print "DOCKS confidence: ",confidence

            except sr.UnknownValueError:
                print("Google Speech Recognition could not understand audio")
            except sr.RequestError as e:
                print("Could not request results from Google Speech Recognition service; {0}".format(e)) 

if __name__ == "__main__":
    os.system('tput reset')
    terminal_name = 'G2P Trainer'
    sys.stdout.write("\x1b]2;"+terminal_name+"\x07")
    #from docks.g2p import GraphemeToPhonemeConverter
#    english_g2p_model = "/home/sysadmin/twiefel/lingorob/g2p_french/g2p_models/model-5"
#    french_g2p_model = "/home/sysadmin/twiefel/lingorob/g2p_french/g2p_models/fr/french.model-1.g2p"
#    #french_g2p_model = "/home/sysadmin/twiefel/lingorob/g2p_french/g2p_models/fr/frenchWords62K.dic.model-1.seq.g2p"
#    g2p_model_path = french_g2p_model
#    g2p = GraphemeToPhonemeConverter(g2p_model_path)
#    
#    english_sentence = "this is a banana"
#    french_sentence = "c'est une banane"
#    sentence = french_sentence
#    print g2p.get_phonemes_for_sentence(sentence)
    multilingual_asr()

    


