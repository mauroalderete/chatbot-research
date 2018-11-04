# -*- coding: utf-8 -*-
import sys
import logging

import nltk
from nltk.corpus import stopwords
from colorama import init
from colorama import Fore
from colorama import Back
from colorama import Style

from intent import Intent
import output
import intentManager

init()

logging.basicConfig(level=logging.INFO) #modos: DEBUG INFO WARNING ERROR CRITICAL
#preparo y configuro los diferentes sistemas de salidas que se utilizaran
outputs = output.Output()
outputs.loadOuput(output.standarOutput())
outputs.loadOuput(output.serialOutput(port="COM6", baudrate=9600))
#preparo y configuro los diferentes sistemas de entrada que se utilizaran

#preparo y cargo las intenciones desde el corpus
intents = intentManager.IntentManager()
### añadir las opciones para realizar o no aprendizaje normal
# forzar el aprendizaje de todo el corpus
# ignorar intents modificados
# guardar cambios en el corpus
# forzar cambio completo en el corpus
a = 0
a = intents.loadCorpus()
if a>0:
    logging.info(str(a)+" intenciones cargadas")
    intents.learnCorpus()
    #ADVERTENCIA: SOLO USAR CUANDO SE CARGA EL CORPUS COMPLETO, de otra forma se sobreescribira todo el corpus y solo grabara los intents cargados
    #intents.updateCorpus()
else:
    sys.exit("Ocurrio un error al cargar el corpus")

print("---CHAT BEGIN---")

print(f'{Back.BLUE}{Fore.WHITE}Human >>{Style.RESET_ALL} ',end="")
text = input()
while text != "bye":
    text = text.lower()
    sentences = nltk.sent_tokenize(text, 'spanish')
    tokens = nltk.word_tokenize(text, 'spanish')
    if (len(sentences) > 1):
        sw = stopwords.words('spanish')
        for token in tokens:
            if token in sw:
                tokens.remove(token)

    potencials = []
    for it in range(len(intents.intents)):
        similarity = intents.intents[it].indexSimilarity(tokens)
        if similarity>0:
            potencials.append([it,similarity])

    def m(e):
        return e[1]
    potencials.sort(reverse=True,key=m)

    if logging.getLogger().getEffectiveLevel()<=logging.INFO:
        print("      Escaneando respuestas posibles...")
        for p in potencials:
            if p[1]==1:
                print(f"      {Fore.GREEN}["+str(p[0])+"] "+str(p[1]) +" => " + intents.intents[p[0]].inputs[0]+f"{Style.RESET_ALL}")
            elif p[1] >=0.75:
                print(f"      {Fore.YELLOW}["+str(p[0])+"] "+str(p[1]) +
                            " => " + intents.intents[p[0]].inputs[0]+f"{Style.RESET_ALL}")
            elif p[1] >= 0.5:
                print(f"      {Fore.MAGENTA}["+str(p[0])+"] "+str(p[1]) +
                            " => " + intents.intents[p[0]].inputs[0]+f"{Style.RESET_ALL}")
            else:
                print(f"      {Fore.RED}["+str(p[0])+"] "+str(p[1]) +
                            " => " + intents.intents[p[0]].inputs[0]+f"{Style.RESET_ALL}")

    print(f'{Back.GREEN}{Fore.WHITE}Ivy >>{Style.RESET_ALL}{Fore.GREEN} ', end="")
    if len(potencials)>0:
        if potencials[0][1]>=0.5:
            print(intents.intents[ potencials[0][0] ].outputs[0])
        else:
            print("Perdon, no entiendo tu pregunta. Podrías intentarlo de nuevo preguntando de otra forma por favor?")
    else:
        print("Perdon, no entiendo tu pregunta. Podrías intentarlo de nuevo preguntando de otra forma por favor?")
    
    print(f'{Back.BLUE}{Fore.WHITE}Human >>{Style.RESET_ALL} ', end="")
    text = input()
print("---CHAT END---")

if __name__ == "__main__":
    print("Ejecutado como Main")
