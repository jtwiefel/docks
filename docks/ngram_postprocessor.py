# -*- coding: utf-8 -*-
"""
Created on Wed Oct 24 14:36:44 2018

@author: twiefel
"""
import requests
from asr_nlp_tools.utils.phoneme_converter import convert_one_char_to_arpabet
def tryPort(port):
    import socket
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    result = False
    try:
        sock.bind(("0.0.0.0", port))
        result = True
        print "Port",port,"is free" 
    except socket.error:
        print "Port",port,"is in use" 
    sock.close()
    return result

class NgramPostprocessor:
    def __init__(self,lm_folder_path, port = "55900", phonemes = False):
        int_port = int(port)
        while not tryPort(int_port):
            int_port = int_port+1
        
        port = str(int_port)
        self.phonemes = phonemes
        
        self.server_url = "http://localhost:"+port+"/"

        import os
        current_path = os.path.dirname(os.path.abspath(__file__))
        print current_path
        
        lm_folder = os.path.abspath(lm_folder_path)        
        print "PHONEMES:",phonemes
        args = " --lm-folder "
        args += lm_folder
        args +=" --model-type "
        args += "ngram"
        args += " --phonemes "
        args += str(phonemes).lower()
        args += " --port "
        args += port
        print args
        
        from threading import Thread
        import subprocess
        def start_docks():
            #print os.popen("java -jar "+current_path+"/docks.jar"+args)
            #self.process = subprocess.Popen("java -jar "+current_path+"/docks.jar"+args, shell=True, stdin=subprocess.PIPE)
            command = "java -jar "+current_path+"/docks.jar"+args
            print "COMMAND",command
            self.process = subprocess.Popen(command.split(), shell=False, stdin=subprocess.PIPE)
            
            #
        thread = Thread(target=start_docks)
        thread.daemon = True
        thread.start()
        
        import time
        while True:
            if not self.phonemes:
                test_sentence = "please bring me a am pizza"
            else:
                test_sentence = ["B","R","IH","NG","SIL",
                                 "M","IY","SIL",
                                 "AH","SIL",
                                 "HH","AE","M","SIL",
                                 "P","IY","T","Z","AH"]
            try:
                self.recognize(test_sentence)
                break
            except:
                pass
                
            print "waiting for docks to start"
            time.sleep(1)
        

    def recognize(self, input_text):
        if input_text == "":
            return ""
        data = input_text
        #print "DATA:",data
        if not self.phonemes:
            if type(input_text) != str:
                print "ERROR"
                print "input must be a text string"
                print "the actual input is",type(input_text)
                raise TypeError
        if self.phonemes:
            if type(input_text) == list:
                data = " ".join(input_text)
            elif type(input_text) == str:
                try: 
                    data = convert_one_char_to_arpabet(input_text)
                    #print hyp_dsc2
                    data = ["SIL" if p==" " else p for p in data]
                    data = " ".join(data)
                except:
                    print "ERROR"
                    print "input must be a list of arpabet phonemes"
                    print "or one-char-phoneme sequence as a string"
                    print "the actual input is",type(input_text)
                    print input_text
                    raise TypeError
            
        #print "PROCESSED DATA:",data
        r = requests.post(self.server_url, data=data)
        return r.text.lower()
    
    def __del__(self):
        print "destroying"
        self.process.terminate()
        
if __name__ == "__main__":
    npp = NgramPostprocessor()
    
    #raw_input()
    test_sentence = "please bring me a am pizza"
    import time
    time.sleep(5)
    for i in range(50):
        print npp.recognize(test_sentence)
        