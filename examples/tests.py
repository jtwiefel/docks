# -*- coding: utf-8 -*-
"""
Created on Wed Dec 19 12:00:51 2018

@author: twiefel
"""
import unittest
import sys
sys.path.append("../../")
class NgramTesting(unittest.TestCase):
    def atest_string(self):
        
        english_sentence_list = "./pizzeria.sentences.txt"
    
    
        new_lm_folder = "./pizzeria"
        #generate n-gram files
        from docks.docks import ngram_generation
        ngram_generation.generate_ngram_language_model(training_sentences_file = english_sentence_list, 
                                                       n_gram_order = 2, 
                                                       new_lm_folder = new_lm_folder)
        
        from docks.docks.ngram_postprocessor import NgramPostprocessor
        ngram_postprocessor = NgramPostprocessor(lm_folder_path = new_lm_folder, phonemes = False)
        #ngram initializiation is non blocking so wait some time
        #import time
        #time.sleep(5)        
        
        test_sentence = "pleas bring mee a han pizza"
        hypothesis = ngram_postprocessor.recognize(test_sentence)
        


        self.assertEqual(hypothesis,"please bring me a ham pizza")

    def atest_string_input_to_phoneme_model(self):
        
        english_sentence_list = "./pizzeria.sentences.txt"
    
    
        new_lm_folder = "./pizzeria"
        #generate n-gram files
        from docks.docks import ngram_generation
        ngram_generation.generate_ngram_language_model(training_sentences_file = english_sentence_list, 
                                                       n_gram_order = 2, 
                                                       new_lm_folder = new_lm_folder)
        
        from docks.docks.ngram_postprocessor import NgramPostprocessor
        ngram_postprocessor = NgramPostprocessor(lm_folder_path = new_lm_folder, phonemes = True)
        #ngram initializiation is non blocking so wait some time
        #import time
        #time.sleep(5)        
        
        test_sentence = "pleas bring mee a han pizza"
        self.assertRaises(TypeError, ngram_postprocessor.recognize, test_sentence)
    
    def atest_phonemes(self):
        
        english_sentence_list = "./pizzeria.sentences.txt"
    
    
        new_lm_folder = "./pizzeria"
        #generate n-gram files
        from docks.docks import ngram_generation
        ngram_generation.generate_ngram_language_model(training_sentences_file = english_sentence_list, 
                                                       n_gram_order = 2, 
                                                       new_lm_folder = new_lm_folder)
        
        from docks.docks.ngram_postprocessor import NgramPostprocessor
        ngram_postprocessor = NgramPostprocessor(lm_folder_path = new_lm_folder, phonemes = True)
        #ngram initializiation is non blocking so wait some time
        #import time
        #time.sleep(5)        
        
        test_sentence = ["B","R","IH","NG","SIL",
                         "M","IY","SIL",
                         "AH","SIL",
                         "HH","AE","M","SIL",
                         "P","IY","T","Z","AH"]
        hypothesis = ngram_postprocessor.recognize(test_sentence)
        self.assertEqual(hypothesis,"bring me a ham pizza")

    def test_one_char_phonemes(self):
        
        english_sentence_list = "./pizzeria.sentences.txt"
    
    
        new_lm_folder = "./pizzeria"
        #generate n-gram files
        from docks.docks import ngram_generation
        ngram_generation.generate_ngram_language_model(training_sentences_file = english_sentence_list, 
                                                       n_gram_order = 2, 
                                                       new_lm_folder = new_lm_folder)
        
        from docks.docks.ngram_postprocessor import NgramPostprocessor
        ngram_postprocessor = NgramPostprocessor(lm_folder_path = new_lm_folder, phonemes = True)
        #ngram initializiation is non blocking so wait some time
        #import time
        #time.sleep(5)        
        
        test_sentence = ["B","R","IH","NG"," ",
                         "M","IY"," ",
                         "AH"," ",
                         "HH","AE","M"," ",
                         "P","IY","T","Z","AH"]
                         
        from asr_nlp_tools.utils.phoneme_converter import convert_arpabet_to_one_char
        test_sentence = convert_arpabet_to_one_char(test_sentence)
        
        hypothesis = ngram_postprocessor.recognize(test_sentence)
        self.assertEqual(hypothesis,"bring me a ham pizza")       

if __name__ == "__main__":
    unittest.main()