# -*- coding: utf-8 -*-

from . import g2p
from pprint import pprint
import numpy as np
import editdistance
import re
import unidecode
def levenshtein(a,b):
    "Calculates the Levenshtein distance between a and b."
    return editdistance.eval(a, b)

def min_levenshtein(input_seq,list_of_seqs):
    best_matching = np.argmin([levenshtein(input_seq, comp_seq) for comp_seq in list_of_seqs])
    return best_matching   

class SentencelistPostprocessor:
    def __init__(self, path_to_sentencelist=None, sentencelist=None, language="english"):
        self.path_to_sentencelist = path_to_sentencelist
        
        assert path_to_sentencelist or sentencelist, "Provide a path to a sentencelist or a sentencelist itself"
        assert not (path_to_sentencelist and sentencelist), "Please Provide either a path or a sentencelist directly"

        if path_to_sentencelist:
            self.path_to_sentencelist = path_to_sentencelist
        elif sentencelist:
            self.sentencelist = [sentence.rstrip("\n") for sentence in sentencelist]

        import os,inspect
        current_path = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))

        if language == "english":
            path_to_g2p_model=current_path+"/../g2p_models/en/english.model-5.g2p"
        elif language == "german":
            path_to_g2p_model=current_path+"/../g2p_models/de/german.model-5.g2p"
        elif language == "french":
            path_to_g2p_model=current_path+"/../g2p_models/fr/french.model-5.g2p"
            
        self.g2p_converter = g2p.GraphemeToPhonemeConverter(path_to_g2p_model)
        self.__parse_phoneme_sequence_list()
                
    def __parse_phoneme_sequence_list(self):
        self.phoneme_sequene_list = []
        if self.path_to_sentencelist:
            self.sentencelist = []
            with open(self.path_to_sentencelist, "r") as f:
                for sentence in f:
                    sentence = sentence.rstrip('\n')
                    self.sentencelist.append(sentence)
                    sentence = sentence.lower()
                    import string
                    table = string.maketrans("","",)
                    #print sentence
                    sentence = sentence.translate(table, string.punctuation)
                    sentence = sentence.decode('utf8')

                    sentence = unidecode.unidecode(sentence)
                    #print type(sentence)
                    #print sentence
                    #pattern = re.compile('[\W_]+')
                    #sentence = pattern.sub('', sentence).lower()
                    self.phoneme_sequene_list.append(self.g2p_converter.get_phonemes_for_sentence(sentence))
        elif self.sentencelist:
            for sentence in self.sentencelist:
                sentence = sentence.lower()
                import string
                table = string.maketrans("","",)
                #print sentence
                sentence = sentence.translate(table, string.punctuation)
                sentence = sentence.decode('utf8')

                sentence = unidecode.unidecode(sentence)
                #print type(sentence)
                #print sentence
                #pattern = re.compile('[\W_]+')
                #sentence = pattern.sub('', sentence).lower()
                self.phoneme_sequene_list.append(self.g2p_converter.get_phonemes_for_sentence(sentence))


    def recognize(self,input_text):
        #print input_text
        #input_text = str(input_text)
        #print input_text
        #print type(input_text)
        input_text = input_text.lower()
        
        #print type(input_text)
        import string
        table = string.maketrans("","")
        #print sentence

        #print sentence
        #input_text = input_text.decode('utf8')
        #print type(input_text)
        input_text = unidecode.unidecode(input_text)
        #print type(input_text)
        input_text = input_text.translate(table, string.punctuation)
        #print type(input_text)
        #print "proce",input_text
        
        input_phonemes = self.g2p_converter.get_phonemes_for_sentence(input_text)
        best_matching = min_levenshtein(input_phonemes, self.phoneme_sequene_list)
        
        dist = levenshtein(input_phonemes,self.phoneme_sequene_list[best_matching])
        confidence = 1.0-min(1,float(dist)/len(self.phoneme_sequene_list[best_matching]))        
        
        return self.sentencelist[best_matching],confidence
        
