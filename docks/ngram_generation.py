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


def generate_ngram_language_model(training_sentences_file, n_gram_order, new_lm_folder):
    from pprint import pprint
    import os
    
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
   
    #from shutil import copyfile
    #copyfile(current_path+"docks_ngram.xml",new_lm_folder+"/docks_ngram.xml")
    
    with open(current_path+"docks_ngram.xml","rb") as f_in:
        with open(new_lm_folder+"/docks_ngram.xml", "wb") as f_out:
            for line in f_in:
                if line.strip().startswith('<property name="dictionaryfile"'):
                    new_line = line.replace("config/dukes/commands.dic", new_lm_path+"/docks_ngram.dic")
                    f_out.write(new_line)
                elif line.strip().startswith('<property name="languagemodelfile"'):
                    new_line = line.replace("config/dukes/commands.lm", new_lm_path+"/docks_ngram.lm")
                    f_out.write(new_line)
                else:
                    f_out.write(line)


    order = n_gram_order
    unknown_token = False
    
    #lm_name = "dukes_bigram"    
    
    
    results_path = new_lm_path+"/"
    if not os.path.isdir(results_path):
        os.mkdir(results_path)
    
    
    
    line_to_end = 2500
    with open(training_sentences_file, 'r') as f:
        with open(results_path +'docks_ngram.sent', 'w') as of:
            for line_number,line in enumerate(f):
                input_command=format_sentence_from_dukes(line)
                if line_number < line_to_end:
                    of.write(" ".join(['<s>']+input_command+['</s>'])+'\n')

    import inspect, os
    current_path = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe()))) 
    env = dict(os.environ)
    env['LD_LIBRARY_PATH'] = current_path+"/"
    #print os.popen(current_path+"/estimate-ngram -text "+results_path+"docks_ngram.sent -write-vocab "+results_path+"docks_ngram.vocab").read()
    command = current_path+"/estimate-ngram -text "+results_path+"docks_ngram.sent -write-vocab "+results_path+"docks_ngram.vocab"
    command = command.split()
    import subprocess
    #process = subprocess.Popen(command, shell=False, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE, env=env)
    error = subprocess.PIPE
    subprocess.Popen(command, shell=False, stdin=subprocess.PIPE, stderr=error, env=env)
    #raw_input()
    if unknown_token:
        with open(results_path +"docks_ngram.vocab", 'a') as of:
            of.write("<unk>\n")
    
    #print os.popen(current_path+"/estimate-ngram -vocab "+results_path+"docks_ngram.vocab -text "+results_path+"docks_ngram.sent -order "+str(order)+" -write-lm "+results_path+"docks_ngram.lm").read()                
    command = current_path+"/estimate-ngram -vocab "+results_path+"docks_ngram.vocab -text "+results_path+"docks_ngram.sent -order "+str(order)+" -write-lm "+results_path+"docks_ngram.lm"
    command = command.split()
    subprocess.Popen(command, shell=False, stdin=subprocess.PIPE, env=env)
    print "finished"
    #pprint(command_list_training)

def generate_ngram_language_model_with_list(training_sentences_file, n_gram_order, new_lm_folder):
    from pprint import pprint
    import os
    
    current_path = os.path.dirname(os.path.abspath(__file__))+"/"
    
    
    if not os.path.exists(new_lm_folder):
        os.makedirs(new_lm_folder)    
    
    new_lm_path = os.path.abspath(new_lm_folder)
   
    with open(current_path+"docks_ngram.xml","rb") as f_in:
        with open(new_lm_folder+"/docks_ngram.xml", "wb") as f_out:
            for line in f_in:
                if line.strip().startswith('<property name="dictionaryfile"'):
                    new_line = line.replace("config/dukes/commands.dic", new_lm_path+"/docks_ngram.dic")
                    f_out.write(new_line)
                elif line.strip().startswith('<property name="languagemodelfile"'):
                    new_line = line.replace("config/dukes/commands.lm", new_lm_path+"/docks_ngram.lm")
                    f_out.write(new_line)
                else:
                    f_out.write(line)


    order = n_gram_order
    unknown_token = False

    results_path = new_lm_path+"/"
    if not os.path.isdir(results_path):
        os.mkdir(results_path)

    line_to_end = 2500
    with open(results_path +'docks_ngram.sent', 'w') as of:
        for line_number,line in enumerate(training_sentences_file):
            input_command=format_sentence_from_dukes(line)
            if line_number < line_to_end:
                of.write(" ".join(['<s>']+input_command+['</s>'])+'\n')

    import inspect, os
    current_path = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe()))) 
    env = dict(os.environ)
    env['LD_LIBRARY_PATH'] = current_path+"/"
    command = current_path+"/estimate-ngram -text "+results_path+"docks_ngram.sent -write-vocab "+results_path+"docks_ngram.vocab"
    command = command.split()
    import subprocess
    error = subprocess.PIPE
    subprocess.Popen(command, shell=False, stdin=subprocess.PIPE, stderr=error, env=env)
    if unknown_token:
        with open(results_path +"docks_ngram.vocab", 'a') as of:
            of.write("<unk>\n")
    
    command = current_path+"/estimate-ngram -vocab "+results_path+"docks_ngram.vocab -text "+results_path+"docks_ngram.sent -order "+str(order)+" -write-lm "+results_path+"docks_ngram.lm"
    command = command.split()
    subprocess.Popen(command, shell=False, stdin=subprocess.PIPE, env=env)
    print "finished"


if __name__ == "__main__":
    import os
    import sys
    os.system('tput reset')
    terminal_name = 'EXPERIMENT'
    sys.stdout.write("\x1b]2;"+terminal_name+"\x07")

    generate_lm()
