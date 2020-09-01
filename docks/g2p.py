# -*- coding: utf-8 -*-
"""
Created on Fri Oct 14 15:06:29 2016

@author: twiefel
"""
import sys
import copy
class GraphemeToPhonemeConverter:
    def __init__(self,model_path):
        import inspect, os
        current_path = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe()))) 
        sys.path.append(current_path+"/sequitur")
        #print sys.path
        import g2p_converter
        self.converter = g2p_converter.g2p_converter(model_path)
        self.phonemes = dict()
    def get_phonemes(self, grapheme_sequence):
        if not grapheme_sequence in self.phonemes.keys():
            try:
                self.phonemes[grapheme_sequence] = self.converter.get_phonemes(grapheme_sequence)
            except:
                print ""
                print "problem with input:",[grapheme_sequence]
                print ""
                raise
        #you have to return a copy, otherwise it will be a reference...
        return copy.deepcopy(self.phonemes[grapheme_sequence])
        
    def get_phonemes_for_sentence(self,sentence):
        phoneme_sequence = []
        for word in sentence.split(" "):
            phoneme_sequence.extend(self.get_phonemes(word))
            phoneme_sequence.append("SIL")
        return phoneme_sequence
        
