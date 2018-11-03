# -*- coding: utf-8 -*-
import hashlib
import json
import logging
import nltk
from nltk.corpus import stopwords
import intent
h="hola múndo como ñ"
print(h)
print(h.encode("utf-8"))
print(h.encode("latin-1"))
print(h.encode("unicode"))
class IntentManager():
    def __init__(self,prhases=[]):
        self.tokensInputs = []
        self.tokensOutputs = []
        self.requiredEntities = []
        self.inputs = []
        self.outputs = []
        
        self.intents = []

        #if (len(prhases)>0):
          #  self.loadIntents(prhases[0],prhases[1])
    
    def loadIntents(self, corpusfile="corpus.json"):

        self.corpusFile = corpusfile
        #chequar excepciones de archivo
        self.file = open(corpusfile,"r")
        self.dataFile = self.file.read()
        self.file.close()
        self.corpusData = json.loads(self.dataFile)
        print(str(self.corpusData))
        ii=0
        for i in self.corpusData["Intents"]:
            print(">>intent ["+str(ii)+"]")
            new = intent.Intent()
            new.inputs = i["inputs"]
            new.outputs = i["outputs"]
            new.emotions = i["emotions"]
            chkText = ''.join(new.inputs) + ''.join(new.outputs)
            checksum = hashlib.md5(chkText.encode('utf-8')).hexdigest()
            if "checksum" in i.keys():
                if checksum == i["checksum"]:
                    print("no aprender. cargando tokens")
                    new.checksum = i["checksum"]
                    new.tokensInputs = i["tokensInputs"]
                    new.tokensOutputs = i["tokensOutputs"]
                else:
                    print("corpus modificado. aprendiendo")
                    new.learnIntent()
                    new.checksum = checksum
            else:
                print("corpus nuevo. aprendiendo")
                new.learnIntent()
                new.checksum = checksum

            self.intents.append( new ) #chequear que realice una copia
        #en este punto se han generado todos los aprendizajes necesarios.
        #y se generaron los checksum pertinentes
        #seria posible actualizar el corpus
        self.updateCorpus()
        
    def updateCorpus(self):
        logging.debug("updateCorpus run")
        ii = 0
        data = {"Intents": [] }
        for i in self.intents:
            data["Intents"].append( {
                "inputs": i.inputs,
                "outputs": i.outputs,
                "emotions": i.emotions,
                "checksum": i.checksum,
                "tokensInputs": i.tokensInputs,
                "tokensOutputs": i.tokensOutputs
            } )
            print(str(data["Intents"][ len(data["Intents"])-1 ]))
            #creo un objeto con la clave "Intents" realizo una copia simbolica de la lista self.intents y genero el json
            #luego grabo el json
            print("updateCorpus JSON::")
            print(json.dumps(data).encode("latin-1"))

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
