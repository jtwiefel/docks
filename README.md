# DOCKS
## How to setup
### Admin Instructions
    sudo apt-get install portaudio19-dev

### User Instructions
DOCKS is using python 2.7

    mkdir docks_example
    cd docks_example
    virtualenv env
    source env/bin/activate
    git clone git@git.informatik.uni-hamburg.de:twiefel/docks.git
    or
    git clone https://git.informatik.uni-hamburg.de/twiefel/docks.git
    pip install -r docks/requirements.txt
    cp -r docks/examples/* .

## How to run
There are examples for the models:

SentenceList

Ngram

Grammar

First, calibrate your microphone:

    pavucontrol
    
Select your microphone using the green arrow. Adjust the volume so that it
shows no activation when you are not speaking, only when you are speaking.

When you start a new terminal always do:

    source env/bin/activate

### Example SentenceList
start it and play around:

    python docks_example_english.py

change the pizzeria.sentences.txt and restart

### Example Ngram
start it and play around:

    python docks_example_ngram.py

change the pizzeria.sentences.txt and restart

### Example Grammar
start it and play around:

    python docks_example_grammar.py

change the icecream.gram and restart

notes:
https://puneetk.com/basics-of-java-speech-grammar-format-jsgf

### Example SentenceList German
start it and play around:

    python docks_example_german.py

change the german.sentences.txt and restart

### Example SentenceList French
start it and play around:

    python docks_example_french.py

change the french.sentences.txt and restart