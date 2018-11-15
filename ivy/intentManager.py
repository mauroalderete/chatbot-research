# -*- coding: utf-8 -*-
import hashlib
import json
import logging
import nltk
from nltk.corpus import stopwords
import intent
class IntentManager():
    def __init__(self,prhases=[]):
        self.__NO_SAVE = 0
        self.__SAVE_ALL = 1
        self.__SAVE_ONLY_CHANGES = 2

        self.tokensInputs = []
        self.tokensOutputs = []
        self.requiredEntities = []
        self.inputs = []
        self.outputs = []
        
        self.intents = []

        self.corpusFile = "corpus.json"

    @property
    def NO_SAVE(self):
        return self.__NO_SAVE
    @property
    def SAVE_ALL(self):
        return self.__SAVE_ALL

    @property
    def SAVE_ONLY_CHANGES(self):
        return self.__SAVE_ONLY_CHANGES
    
    def loadCorpus(self,
    corpusFile="corpus.json",
    ignore_modified_intents=False,
    ignore_new_intents=False,
    ignore_learned_intents=False):
        """Carga el archivo de datos del corpus que debe manejar el chatbot
        
        Keyword Arguments:
            corpusFile {str} -- Ruta y nombre del archivo json que contiene el corpus (default: {"corpus.json"})
            ignore_modified_intents {bool} -- Si se debe ignorar los intents que se encuentran modificados (default: {False})
            ignore_new_intents {bool} -- Ignora los intents añadidos recientemente (default: {False})
            ignore_learned_intents {bool} -- Ignora los intents que ya fueron parseados (default: {False})
        
        Returns:
            integer -- Retorna la cantidad de intents cargados
        """

        #corpusFile: ubicación y nombre del archivo que contiene el corpus
        #ignore_modified_intents: ignorar del corpus los intents modificados, si vale false los incorpora y los aprende
        #ignore_new_intents: ignorar del corpus los intentes nuevos, si vale false los incporora y los aprende
        #ignore_learned_intents: ignorar del corpus los intents que no requieren aprendizaje
        logging.debug("LOADINTENTS")
        
        self.corpusFile = corpusFile
        try:
            self.file = open(self.corpusFile,"r", encoding="utf-8")
        except FileNotFoundError:
            logging.critical("Archivo de Corpus no encontrado. Se cancela la carga de corpus")
            logging.info("path: "+self.corpusFile)
            return -1 #generar excepcion

        try:
            self.dataFile = self.file.read()
        except FileNotFoundError:
            logging.critical("No se puede leer el Archivo de Corpus. Se cancela la carga de corpus")
            return -1  # generar excepcion

        self.file.close()
        self.corpusData = json.loads(self.dataFile)
        intentsLoaded = 0
        for i in self.corpusData["Intents"]:
            loadIntent = True
            new = intent.Intent()
            if "checksum" in i.keys():
                new.inputs = i["inputs"]
                new.outputs = i["outputs"]
                new.emotions = i["emotions"]
                chkText = ''.join(new.inputs) + ''.join(new.outputs)+''.join(new.emotions)
                checksum = hashlib.md5(chkText.encode('utf-8')).hexdigest()
            
                if checksum == i["checksum"]:
                    if ignore_learned_intents is False:
                        logging.debug("Loading learned intent")
                        new.checksum = i["checksum"]
                        new.tokensInputs = i["tokensInputs"]
                        new.tokensOutputs = i["tokensOutputs"]
                        new.learningState = new.LEARNED_INTENT
                    else:
                        logging.debug("Ignoring learned intent")
                        loadIntent = False
                else:
                    if ignore_modified_intents is False:
                        logging.debug("Loading modified intent")
                        new.learningState = new.MODIFIED_INTENT
                        new.checksum = checksum
                    else:
                        logging.debug("Ignoring modified intent")
                        loadIntent = False
            else:
                if ignore_new_intents is False:
                    logging.debug("Loading new intent")
                    new.learningState = new.NEW_INTENT
                    new.checksum = checksum
                else:
                    logging.debug("Ignoring new intent")
                    loadIntent = False
            if loadIntent:
                self.intents.append( new ) #chequear que realice una copia
                intentsLoaded = intentsLoaded + 1
        return intentsLoaded

    def learnCorpus(self, force_learning=False):
        #force_learning: ejecuta el aprendizaje para todos los intents
        logging.debug("+++++LEARNCORPUS")
        for i in self.intents:
            if i.learningState!=i.LEARNED_INTENT or ( i.learningState==i.LEARNED_INTENT and force_learning ):
                i.normalizeInputs()
                i.normalizeOutputs()
                i.learnIntent()
        
    def updateCorpus(self):
        logging.debug("updateCorpus run")
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
        logging.debug("JSON dump::")
        a=json.dumps(data, indent=4, sort_keys=True, ensure_ascii=False)
        logging.debug("Corpus Save")
        logging.debug(a)
        #chequar excepciones de archivo
        self.file = open(self.corpusFile, "w", encoding="utf-8")
        self.file.write(a)
