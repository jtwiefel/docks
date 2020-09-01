# -*- coding: utf-8 -*-
"""
Created on Wed Oct 24 14:36:44 2018

@author: twiefel
"""
import requests
class GrammarPostprocessor:
    def __init__(self,lm_folder_path, port = "55001"):
        self.server_url = "http://localhost:"+port+"/"
        
        import os
        current_path = os.path.dirname(os.path.abspath(__file__))
        print current_path
        
        lm_folder = os.path.abspath(lm_folder_path)        
        
        args = " --lm-folder "
        args += lm_folder
        args +=" --model-type "
        args += "grammar"
        args += " --phonemes "
        args += "false"
        args += " --port "
        args += port
        print args
        
        from threading import Thread
        import subprocess
        def start_docks():
            #print os.popen("java -jar "+current_path+"/docks.jar"+args)
            #self.process = subprocess.Popen("java -jar "+current_path+"/docks.jar"+args, shell=True, stdin=subprocess.PIPE)
            command = "java -jar "+current_path+"/docks.jar"+args
            self.process = subprocess.Popen(command.split(), shell=False, stdin=subprocess.PIPE)
            
            #
        thread = Thread(target=start_docks)
        thread.daemon = True
        thread.start()
        

    def recognize(self, input_text):
        r = requests.post(self.server_url, data=input_text)
        return r.text.lower()
    
    def __del__(self):
        print "destroying"
        self.process.terminate()
        
if __name__ == "__main__":
    npp = GrammarPostprocessor()
    
    #raw_input()
    test_sentence = "please bring me a am pizza"
    import time
    time.sleep(5)
    for i in range(50):
        print npp.recognize(test_sentence)
        