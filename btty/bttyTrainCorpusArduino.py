# -*- coding: utf-8 -*-

from chatterbot import ChatBot

def mergeList(leftList, rightList, innerExp=None, innerList=False):
    if innerList:
        z = [[y+str(innerExp)+x] for y in leftList for x in rightList]
    else:
        z = [ y+str(innerExp)+x for y in leftList for x in rightList ]

    return z

def concatList(leftList, rightList):
    r = []
    l = list(map(lambda x: list(map(lambda y: [y, x], leftList)), rightList))
    list(map(lambda x: r.extend(x), l))
    return r

def extendList(leftList, rightList):

    r = []
    l = list(map(lambda x: list(map(lambda y: y+[x], leftList)), rightList))
    list(map(lambda x: r.extend(x), l))
    return r

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

headers = [
    'Dejame ver...',
    'Veamos    ...'
]

footers = [
    'Entendiste?',
]

apologies = [
    'Perdon, tu pregunta me ha superado. Mejor llama al profesor.',
]

affirmativeResponse = [
    'Gracias',
]

negativeResponse = [
    'casi',
    'no entiendo',
    'no',
]

affirmativeExclamation = [
    'Excelente'
]

class Theme:
    question = []
    answers = []
    answersComplex = []


themes = []

themes.append(Theme())
last = len(themes)-1
themes[last].question = [
    '¿que es arduino?',
]
themes[last].answers.append(
    [
        '0 Arduino es una placa',
    ]
)
themes[last].answers.append(
    [
        '1 Arduino es esto',
    ]
)
themes[last].answers.append(
    [
        '2 Arduino es un robot!!',
    ]
)

talks=[]
conversations=[]

print("Loading corpus...", end="")

for t in themes:
    #Preparo las respuestas complejas, combinando los headers con los footers
    for a in t.answers:
        t.answersComplex.append( mergeList(mergeList(headers, a, innerExp=", "), footers, innerExp=". ") )
    #Preparo las preguntas para que queden sus elementos en listas internas
    z=[]
    for q in t.question:
        z.append([q])
    t.question = z.copy()

print("[OK]")

print("Generating conversations...", end="")
for t in themes:
    conversationPreview = t.question
    conversationPreviewAuxiliar = []
    last = len(t.answersComplex)
    print("last: "+str(last))
    for iac in range(last):
        conversationPreview = extendList(conversationPreview, t.answersComplex[iac])
        conversations.extend(extendList(extendList(conversationPreview, affirmativeResponse),affirmativeExclamation))

        if (iac == last-1):
            conversations.extend( extendList( extendList(conversationPreview, negativeResponse), apologies))
        else:
            conversationPreview = extendList(conversationPreview, negativeResponse)
print("[OK]")
print("Satdistics")
print("headers: "+str(len(headers)))
print("footers: "+str(len(footers)))
print("affirmativeResponse: "+str(len(affirmativeResponse)))
print("affirmativeExclamation: "+str(len(affirmativeExclamation)))
print("negativeResponse: "+str(len(negativeResponse)))
print("apologies: "+str(len(apologies)))
print("themes: "+str(len(themes)))
print("conversations: "+str(len(conversations)))

print(">>Training "+str(len(conversations))+" conversations")
cmd = input("ver resumen? Y/n")
if (cmd is "Y"):
    [print(x) for x in conversations]
cmd=input("empezar? Y/n")
if (cmd is "Y"):
    for c in conversations:
        btty.train(c)
    print("Btty training corpus Arduino finish")
else:
    print("la proxima será")
