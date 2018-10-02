# -*- coding: utf-8 -*-

from chatterbot import ChatBot

btty = ChatBot(
    'Btty',
    storage_adapter='chatterbot.storage.SQLStorageAdapter',
    input_adapter='chatterbot.input.TerminalAdapter',
    output_adapter='chatterbot.output.TerminalAdapter',
    preprocessors=[
        'chatterbot.preprocessors.clean_whitespace',
        'chatterbot.preprocessors.unescape_html',
        'chatterbot.preprocessors.convert_to_ascii'
    ],
    database='./btty0.sqlite3',
    trainer="chatterbot.trainers.ListTrainer",
)

pasiveGreeting = [
    'hola',
    'buenos dias',
    'bon dia',
    'saludos',
    'buen dia',
    'holas van, holas vienen'
]

activeQuestion = [
    'decime en que puedo ayudarte?',
    'preguntame lo que necesites saber',
    'que duda tenes?',
    'decime como puedo ayudarte?',
    'contame y tratare de ayudarte'
]
'''
pasiveQuestion = [
    'tengo una duda',
    'pregunta',
    '...',
    'una pregunta',
    'duda',
    'una duda',
    'ayuda',
    'necesito ayuda',
    'me das una mano',
    'me das una mano?',
    'una mano',
    'una mano?',
    'ayudaaa',
    'por favor',
    'pls',
    'help',
    'helpme',
    'podes ayudarme',
    'necesito ayuda',
    'necesito resolver algo',
    'necesito una mano',
    'necesito una orientacion',
    'estoy desorientado',
    'estoy perdido',
    'hay algo que no entiendo',
    'no entiendo',
    'me olvide',
]
'''
activeIncite = [
    'ok',
    'estoy para ayudarte',
    'por supuesto',
    'soy todo oidos',
    'todos nos desorientamos alguna vez',
]

responseIncite = []
for i in activeIncite:
    for q in activeQuestion:
        responseIncite.append( i+', '+q )

activeGreeting = []

for q in activeQuestion:
    for g in pasiveGreeting:
        activeGreeting.append( g+', '+q )
        #print(activeGreeting[len(activeGreeting)-1 ])

#I[""]O[activeGreeting]
#I[""]O[pasiveGreeting]
#I[pasiveGreeting]O[activeGreeting]
#I[pasiveGreeting]O[activeGreeting]
#I[pasiveQuestion]O[activeIncite]
#I[pasiveGreetingpasiveQuestion]O[pasiveGreetingactiveIncite]

talks = []
print(">>Loading I[""]O[activeGreeting]")
for r in activeGreeting:
    talks.append(['',r])
    print("human: "+talks[len(talks)-1][0]+" btty: " + talks[len(talks)-1][1])
print(">>Loading I[""]O[pasiveGreeting]")
for r in pasiveGreeting:
    talks.append(['', r])
    print("human: "+talks[len(talks)-1][0]+" btty: " + talks[len(talks)-1][1])
print(">>Loading I[pasiveGreeting]O[activeGreeting]")
for i in pasiveGreeting:
    for r in activeGreeting:
        talks.append([i, r])
        print("human: "+talks[len(talks)-1][0]+" btty: " + talks[len(talks)-1][1])
'''
print(">>Loading I[pasiveQuestion]O[responseIncite]")
for q in pasiveQuestion:
    for i in responseIncite:
        talks.append([q, i])
        print("human: "+talks[len(talks)-1][0] +" btty: " + talks[len(talks)-1][1])
'''
print(">>Training")
for t in talks:
    btty.train( t )

print("Btty training corpus Saludos finish")
