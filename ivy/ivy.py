# -*- coding: utf-8 -*-
import nltk
from nltk.corpus import stopwords

class CIntent:
    def __init__(self,inputs,outputs):
        self.tokensInputs = []
        self.tokensOutputs = []
        self.requiredEntities = []

        self.inputs = inputs.copy()
        self.outputs = outputs.copy()
        self.normalizeInputs()
        self.normalizeOutputs()

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
    
    def indexSimilarity(self, tokens):
        lenTokens = len(tokens)
        lenTokensSimilar = 0
        for tt in tokens:
            if tt in self.tokensInputs:
                lenTokensSimilar = lenTokensSimilar + 1
        return lenTokensSimilar/lenTokens

intents = []
inputs = [
    'que es arduino',
    'arduino, que es',
    'arduino que es',
    'arduino',
]
outputs = [
    'Arduino es una plataforma de hardware libre, basada en una placa con un microcontrolador y un entorno de desarrollo (software), diseñada para facilitar el uso de la electrónica en proyectos multidisciplinares. Arduino es una plataforma abierta que facilita la programación de un microcontrolador.'
]
intents.append(CIntent(inputs,outputs))

inputs = [
    'donde compro un arduino',
    'como consigo un arduino',
    'como compro un arduino',
    'donde puedo comprar un arduino',
    'donde compro arduino',
    'como consigo arduino',
    'como compro arduino',
    'donde puedo comprar arduino',
]
outputs = [
    'Se puede comprar arduino en tiendas de electronica que vendan componentes e instrumentación de electrónica. Tambien es posible comprar por internet. La oferta es variada y suele haber un sitio donde los precios son suficientemente economicos como para tenerlos en cuenta.'
]

intents.append(CIntent(inputs,outputs))

inputs = [
    'Cuantas versiones de arduino hay',
    'cuales son las versiones de arduino',
    'arduino tiene versiones',
    'que versiones de arduino hay',
    'que versiones de arduino existen',
    'cuantas versiones de arduino existen',
    'existen muchas versiones de arduino',
]
outputs = [
    'Arduino dispone de una gran familia de versiones. Año tras año se desarrollan nuevas versiones que implementan mejoras en los modelos ya existentes y se diseñan nuevos arduinos con funcionalidades interesantes. En la web de arduino existe todo un catalogo sobre los modelos. Tambien existen los arduino fork, que son generalmente de producción china y de bajo costo'
]

intents.append(CIntent(inputs, outputs))

tokens = []
for it in intents:
    print("INTENT with "+str(len(it.inputs))+" inputs", end="")
    for inp in it.inputs:
        sent = nltk.sent_tokenize(inp,'spanish')
        tokens = nltk.word_tokenize(inp, 'spanish')
        if (len(sent) > 1):
            sw = stopwords.words('spanish')
            for token in tokens:
                if token in sw:
                    tokens.remove(token)
        for token in tokens:
            if token not in it.tokensInputs:
                it.tokensInputs.append(token)

    print("TOKENS "+str(it.tokensInputs))

print("---CHAT BEGIN---")
text = input('>>')
while text != "bye":
    text = text.lower()
    sent = nltk.sent_tokenize(text, 'spanish')
    tokens = nltk.word_tokenize(text, 'spanish')
    print("  "+str(len(sent))+" oraciones")
    print("  tokens>>"+str(tokens))
    if (len(sent) > 1):
        sw = stopwords.words('spanish')
        for token in tokens:
            if token in sw:
                tokens.remove(token)

    potencials = []
    for it in range(len(intents)):
        potencials.append([it,intents[it].indexSimilarity(tokens)])
    def m(e):
        print("    intencion: "+str(e[0])+" index: "+str(e[1]))
        return e[1]
    potencials.sort(reverse=True,key=m)
    if potencials[0][1]>0.5:
        print("ivy>> "+intents[ potencials[0][0] ].outputs[0])
    else:
        print("ivy>> No comprendo podría preguntar nuevamente")
    text = input('>>')

print("---chat end---")

if __name__ == "__main__":
    print("Ejecutado como Main")
