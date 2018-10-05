# -*- coding: utf-8 -*-
import nltk
from nltk.corpus import stopwords
from intent import Intent

intents = []
intents.append(Intent([[
    'que es arduino',
    'arduino, que es',
    'arduino que es',
    'arduino',
],
    [
    'Arduino es una plataforma de hardware libre, basada en una placa con un microcontrolador y un entorno de desarrollo (software), diseñada para facilitar el uso de la electrónica en proyectos multidisciplinares. Arduino es una plataforma abierta que facilita la programación de un microcontrolador.'
]]))
intents.append(Intent([[
    'que sabes sobre arduino',
    'que conoces sobre arduino',
    'sabes cosas de arduino',
    'sabes de arduino',
    'conoces el arduino',
    'que conoces de arduino',
    'que sabes de arduino',
],
    [
    'Se muchas cosas de arduino. Como se programa, que se usa para programar, donde comprar, que versiones hay'
]]))
intents.append(Intent([[
    'que sabes sobre arduino uno',
    'que conoces sobre arduino uno',
    'sabes cosas de arduino uno',
    'sabes de arduino uno',
    'conoces el arduino uno',
    'que conoces de arduino uno',
    'que sabes de arduino uno',
    'que es arduino uno',
],
    [
    'Arduino UNO, es la plataforma de excelencia para iniciarse en el mundo de Arduino y el desarrollo de las nuevas tecnologias. Si recien empezas a conocer sobre este facinante mundo no dudes en empezar con un Arduino UNO.'
]]))
intents.append(Intent([[
    'hola',
    'buenos dias',
    'buenos días',
    'que tal',
    'que onda',
    'todo bien'
],
    [
    'hola, en que puedo ayudarte?'
]]))
intents.append(Intent([[
    'sos un robot',
    'sos un chatbot',
    'quien sos',
    'que sos',
    'sos humano',
    'como te llamas'
    'cual es tu nombre'
],
    [
    'Soy Ivy, un prototipo de IA conversacional creado para hablar sobre arduino y ayudarte a resolver tus dudas'
]]))
intents.append(Intent([[
    'como se programa arduino',
    'como se programa una placa arduino',
    'como se programan los arduinos',
],
    [
    'Para programar una placa arduino se necesita un editor de codigo. El más popular es el Arduino IDE creado por las mismas personas que crearon el Arduino. Pero tambien es posible utilizar otros entornos, aunque no te lo recomendaría si es que recien estas empezando.'
]]))
intents.append(Intent([[
    'en que lenguaje se programa arduino',
    'que lenguajes se pueden usar para programar arduino',
    'que lenguaje de programación funciona con arduino',
    'que lenguaje de programación se usa para arduino',
],
    [
    'Para programar Arduino suele usarse el lenguaje de programación C/C++. Existen otras alternativas, algunas más desarrolladas que otras. Pero C/C++ sigue siendo el estandar más popular. De hecho, la mayoría de las librearias estan escritos en este lenguaje'
]]))
intents.append(Intent([[
    'para que sirve el arduino',
    'para que sirve arduino',
    'para que sirve la placa arduino',
    'de que sirve arduino',
    'de que sirve la placa arduino'
],
    [
    'Arduino es una plataforma que tiene muchos propositos. Fue diseñada en principio para impulsar la Internet de Las Cosas, pero en poco tiempo se popularizo en educación. Actualmente miles de personas utilizan Arduino en diferentes proyectos, muchos para aprender programación y electronica, y muchos otros para construir sus propia tecnología y ayudar a que su entorno sea un lugar mejor.'
]]))
intents.append(Intent([[
    'donde compro un arduino',
    'como consigo un arduino',
    'como compro un arduino',
    'donde puedo comprar un arduino',
    'donde compro arduino',
    'como consigo arduino',
    'como compro arduino',
    'donde puedo comprar arduino',
    'donde venden arduinos',
    'donde venden la placa arduino',
    'donde los venden',
    'donde venden los arduinos',
], [
    'Se puede comprar arduino en tiendas de electronica que vendan componentes e instrumentación de electrónica. Tambien es posible comprar por internet. La oferta es variada y suele haber un sitio donde los precios son suficientemente economicos como para tenerlos en cuenta.'
]]))
intents.append(Intent([[
    'Cuantas versiones de arduino hay',
    'cuales son las versiones de arduino',
    'arduino tiene versiones',
    'que versiones de arduino hay',
    'que versiones de arduino existen',
    'cuantas versiones de arduino existen',
    'existen muchas versiones de arduino'
],[
    'Arduino dispone de una gran familia de versiones. Año tras año se desarrollan nuevas versiones que implementan mejoras en los modelos ya existentes y se diseñan nuevos arduinos con funcionalidades interesantes. En la web de arduino existe todo un catalogo sobre los modelos. Tambien existen los arduino fork, que son generalmente de producción china y de bajo costo'
]]))

'''
*********************************************************************************
'''
print("---CHAT BEGIN---")
text = input('human>> ')
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
    for it in range(len(intents)):
        potencials.append([it,intents[it].indexSimilarity(tokens)])
    def m(e):
        print("    intencion: "+str(e[0])+" index: "+str(e[1]))
        return e[1]
    potencials.sort(reverse=True,key=m)

    if potencials[0][1]>0.5:
        print("ivy>> "+intents[ potencials[0][0] ].outputs[0])
    else:
        print("ivy>> Perdon, no entiendo tu pregunta. Podrías intentarlo de nuevo preguntando de otra forma por favor?")
    text = input('human>> ')
print("---chat end---")

if __name__ == "__main__":
    print("Ejecutado como Main")
