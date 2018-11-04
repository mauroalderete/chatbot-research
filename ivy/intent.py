# -*- coding: utf-8 -*-
import logging

import nltk
from nltk.corpus import stopwords

class Intent():
    def __init__(self,prhases=[]):
        self.tokensInputs = []
        self.tokensOutputs = []
        self.inputs = []
        self.outputs = []
        self.emotions = []
        self.checksum = ""

        self.__MODIFIED_INTENT = 1
        self.__NEW_INTENT = 2
        self.__LEARNED_INTENT = 3

        self.learningState = None

    @property
    def MODIFIED_INTENT(self):
        return self.__MODIFIED_INTENT

    @property
    def NEW_INTENT(self):
        return self.__NEW_INTENT

    @property
    def LEARNED_INTENT(self):
        return self.__LEARNED_INTENT

    def normalizeInputs(self):
        temp = []
        for i in self.inputs:
            logging.debug("INPUT::"+str(i))
            i = i.lower()
            temp.append(i)
            
        self.inputs.clear()
        self.inputs.extend(temp)
    
    def normalizeOutputs(self):
        temp = []
        for o in self.outputs:
            o = o.lower()
            temp.append(o)
        self.outputs.clear()
        self.outputs.extend(temp)

    def learnIntent(self):
        logging.debug("************************************LEARINTENT")
        sw = stopwords.words('spanish')

        for inp in self.inputs:
            sentences = nltk.sent_tokenize(inp, 'spanish')
            tokenInput = nltk.word_tokenize(inp, 'spanish')

            logging.debug(">>senteces:"+str(sentences))
            logging.debug(">>tokenInputs:"+str(tokenInput))
            #print("["+inp+"]"+str(len(sentences))+"sentences")
            #print("    "+str(self.tokensInputs))
            if (len(sentences) > 1):
                #print("    clean stopwords")
                for token in self.tokensInputs:
                    if token in sw:
                        tokenInput.remove(token)
            for token in tokenInput:
                if token not in self.tokensInputs:
                    self.tokensInputs.append(token)
    
    def indexSimilarity(self, tokens):
        lenTokens = len(tokens)
        lenTokensSimilar = 0
        for tt in tokens:
            if tt in self.tokensInputs:
                lenTokensSimilar = lenTokensSimilar + 1
        return lenTokensSimilar/lenTokens
