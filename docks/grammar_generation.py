# -*- coding: utf-8 -*-
"""
Created on Wed Mar 14 14:34:17 2018

@author: twiefel
"""

def format_sentence_from_dukes(sentence):
    import re
    sentence = sentence.strip('\n')
  
    sentence = sentence.replace('.', ' . ')
    sentence = sentence.replace('-', ' - ')
    sentence = sentence.replace(',', ' , ')
    sentence = sentence.strip()
    sentence = sentence.lower()
    sentence = sentence.upper()
    sentence = re.sub(' +',' ',sentence)
    #sentence=' '.join(input_command.split())
    sentence=sentence.split()

    #print sentence
    #raw_input()
    return sentence

    
def generate_grammar_language_model(jsgf_grammar_file, new_lm_folder):
    from pprint import pprint
    import os
    from shutil import copyfile    
    #training_sentences_path = training_sentences_file.split("/")[:-1]
    #results_path = os.path.dirname(os.path.abspath(training_sentences_file))+"/"
    #print training_sentences_path
    #results_path = training_sentences_path
    #print results_path
    #raise
    current_path = os.path.dirname(os.path.abspath(__file__))+"/"
    
    
    if not os.path.exists(new_lm_folder):
        os.makedirs(new_lm_folder)    
    
    new_lm_path = os.path.abspath(new_lm_folder)
    print new_lm_path
   

    copyfile(jsgf_grammar_file, new_lm_folder+"/docks_grammar.gram")
    
    with open(current_path+"docks_grammar.xml","rb") as f_in:
        with open(new_lm_folder+"/docks_grammar.xml", "wb") as f_out:
            for line in f_in:
                if line.strip().startswith('<property name="dictionaryfile"'):
                    new_line = line.replace("config/dukes_gram/model/docks_grammar.dic", new_lm_path+"/docks_grammar.dic")
                    f_out.write(new_line)
                elif line.strip().startswith('<property name="grammarpath"'):
                    new_line = line.replace("config/dukes_gram/model/", new_lm_path+"/")
                    f_out.write(new_line)
                else:
                    f_out.write(line)

def generate_grammar_language_model_with_list(jsgf_grammar_tmp, new_lm_folder):
    from pprint import pprint
    import os
    from shutil import copyfile    
    #training_sentences_path = training_sentences_file.split("/")[:-1]
    #results_path = os.path.dirname(os.path.abspath(training_sentences_file))+"/"
    #print training_sentences_path
    #results_path = training_sentences_path
    #print results_path
    #raise
    current_path = os.path.dirname(os.path.abspath(__file__))+"/"
    
    
    if not os.path.exists(new_lm_folder):
        os.makedirs(new_lm_folder)    
    
    new_lm_path = os.path.abspath(new_lm_folder)

    new_file = open(new_lm_folder+"/docks_grammar.gram", "w+")
    new_file.writelines(jsgf_grammar_tmp)
    new_file.close()

    with open(current_path+"docks_grammar.xml","rb") as f_in:
        with open(new_lm_folder+"/docks_grammar.xml", "wb") as f_out:
            for line in f_in:
                if line.strip().startswith('<property name="dictionaryfile"'):
                    new_line = line.replace("config/dukes_gram/model/docks_grammar.dic", new_lm_path+"/docks_grammar.dic")
                    f_out.write(new_line)
                elif line.strip().startswith('<property name="grammarpath"'):
                    new_line = line.replace("config/dukes_gram/model/", new_lm_path+"/")
                    f_out.write(new_line)
                else:
                    f_out.write(line)

if __name__ == "__main__":
    import os
    import sys
    os.system('tput reset')
    terminal_name = 'EXPERIMENT'
    sys.stdout.write("\x1b]2;"+terminal_name+"\x07")

