#!/usr/bin/env python


import math, sets, sys

import SequiturTool
from sequitur import Translator
from misc import gOpenIn, gOpenOut, set
from sys import stdout
from collections import namedtuple

def run():  
    print 'Hello world!'    
    self.main()

def loadG2PSample(fname):
    if fname == '-':
        sample = loadPlainSample(fname)
    else:
        firstLine = gOpenIn(fname, defaultEncoding).readline()
    if firstLine.startswith('<?xml'):
        sample = [ (tuple(orth), tuple(phon))
               for orth, phon in loadBlissLexicon(fname) ]
    else:
        sample = loadPlainSample(fname)
    return sample

def readApply(fname):
    for line in gOpenIn(fname, defaultEncoding):
        word = line.strip()
        #print word
        left = tuple(word)
        #print line
        yield word, left

def readArray(name):
    for word in name:
        #print word
        left = tuple(word)
        #print left
        yield word, left

def main(*javatuple):
    #print 'in main'
    #lst = list(javatuple)
    #lst[0] = 'dulli'
    #javatuple = tuple(lst)

    #words = readApply('args.txt')
    words = readArray(javatuple)
    print words
    #print 'printing words'
    #print words
    #print 'printing classname'
    #print words.__class__.__name__
    wantVariants = False
    #print 'iterating worrds'
    res=list()
    words = "hello mister roboto".split(" ")
    

    for word in words:
        left = tuple(word)
        #print word,left
        try:
            if wantVariants:
                totalPosterior = 0.0
                nVariants = 0
                nBest = translator.nBestInit(left)
                while totalPosterior < threshold and nVariants < nVariantsLimit:
                    try:
                        logLik, result = translator.nBestNext(nBest)
                    except StopIteration:
                        break
                        posterior = math.exp(logLik - nBest.logLikTotal)
                        #print >> stdout, ('%s\t%d\t%f\t%s' % \
                        #   (word, nVariants, posterior, ' '.join(result)))
                        totalPosterior += posterior
                        nVariants += 1
            else:
                result = translator(left)
                #print >> stdout, ('%s\t%s' % (word, ' '.join(result)))
                re=('%s\t%s' % (word, ' '.join(result)))
                #print re
                res.append(('%s   %s' % (word, ' '.join(result))).encode('ascii','ignore'))

        except translator.TranslationFailure, exc:
            try:
                print >> stderr, 'failed to convert "%s": %s' % (word, exc)
            except:
                pass
    
    #print 'end main'
    print res
    return res



class g2p_converter:
    def __init__(self, model_path):
        class options(object):
            pass  
        options = options()
        options.testSample = None
        options.modelFile = model_path  
        options.trainSample = None  
        options.encoding = 'ISO-8859-15'  
        options.shouldInitializeWithCounts = None  
        options.psyco = None  
        options.stack_limit = None  
        options.shouldTranspose = None  
        options.applySample = 'args.txt'  
        options.shouldRampUp = None  
        options.resume_from_checkpoint = None  
        options.lengthConstraints = None  
        options.checkpoint = None  
        options.eager_discount_adjustment = None  
        options.fakeTranslator = None  
        options.tempdir = None  
        options.profile = None  
        options.variants_number = None  
        options.maxIterations = 100  
        options.testResult = None  
        options.variants_mass = None  
        options.shouldSuppressNewMultigrams = None  
        options.develSample = None  
        options.shouldWipeModel = None  
        options.resource_usage = None  
        options.test_segmental = None  
        options.fixed_discount = None  
        options.newModelFile = None  
        options.minIterations = 20  
        options.shouldSelfTest = None  
        options.viterbi = None  
        options.shouldTestContinuously = None  
        options.phoneme_to_phoneme = None
        
        import codecs
        global defaultEncoding
        defaultEncoding = options.encoding
        global stdout, stderr
        encoder, decoder, streamReader, streamWriter = codecs.lookup(options.encoding)
        stdout = streamWriter(sys.stdout)
        stderr = streamWriter(sys.stderr)
        loadSample = loadG2PSample
        model = SequiturTool.procureModel(options, loadSample, log=stdout)
        self.translator = Translator(model)
    def get_phonemes(self, word):
        res = self.translator(tuple(word))
        return ' '.join(res).encode('ascii','ignore').split(" ")

if __name__ == '__main__':
    converter = g2p_converter()
    print converter.get_phonemes("take")


    #main(('hallo','mister','roboto'))
