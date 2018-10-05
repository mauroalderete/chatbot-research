# -*- coding: utf-8 -*-
import nltk
from nltk.corpus import stopwords
from intent import Intent

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
intents.append(Intent([inputs,outputs]))
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
intents.append(Intent([inputs, outputs]))
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
intents.append(Intent([inputs, outputs]))
print("---CHAT BEGIN---")
text = input('human>> ')
while text != "bye":
    text = text.lower()
    sentences = nltk.sent_tokenize(text, 'spanish')
    tokens = nltk.word_tokenize(text, 'spanish')
    print("body>>tokens "+str(tokens))
    if (len(sentences) > 1):
        print("body>>mas de una oracion")
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
    text = input('human>> ')
print("---chat end---")

if __name__ == "__main__":
    print("Ejecutado como Main")
