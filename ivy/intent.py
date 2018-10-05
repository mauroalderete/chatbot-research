# -*- coding: utf-8 -*-
import nltk
from nltk.corpus import stopwords

class Intent():
    def __init__(self,prhases=[]):
        self.tokensInputs = []
        self.tokensOutputs = []
        self.requiredEntities = []
        self.inputs = []
        self.outputs = []

        if (len(prhases)>0):
            self.loadIntent(prhases[0],prhases[1])
    
    def loadIntent(self, inputs, outputs):
        self.tokensInputs = []
        self.tokensOutputs = []
        self.requiredEntities = []

        self.inputs = inputs.copy()
        self.outputs = outputs.copy()
        self.normalizeInputs()
        self.normalizeOutputs()
        self.learnIntent()

    def normalizeInputs(self):
        temp = []
        for i in self.inputs:
            i = i.lower()
            temp.append(i)
            temp.append('¿'+i+'?')
            temp.append(i+'?')
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
        print("learnIntent")
        for inp in self.inputs:
            sentences = nltk.sent_tokenize(inp, 'spanish')
            tokenInput = nltk.word_tokenize(inp, 'spanish')
            print("["+inp+"]"+str(len(sentences))+"sentences")
            print("    "+str(self.tokensInputs))
            if (len(sentences) > 1):
                print("    clean stopwords")
                sw = stopwords.words('spanish')
                '''
                que sucede si en la lista de tokens hay mas de un stopword
                '''
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
