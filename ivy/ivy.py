# -*- coding: utf-8 -*-
import nltk
from nltk.corpus import stopwords

class CIntent:
    def __init__(self):
        self.tokensInputs = []
        self.tokensOutputs = []
        '''
        este dato servira mas adelante para la construcción de conversaciones sostenidas
        la idea es que se enumeren los datos que son requeridos para satisfacer la intención
        y si no estan satisfechos, entonces el motor de dialogo debera solicitar esos datos
        Se podría construir como una lista (id, labels: ('','',''), regex=('##.#','*0','0?.*') )
        '''
        self.requiredEntities = []

        self.inputs = [
            'que es arduino',
            'arduino, que es',
            'arduino que es',
            'arduino',
        ]
        self.outputs = [
            'Arduino es una plataforma de hardware libre, basada en una placa con un microcontrolador y un entorno de desarrollo (software), diseñada para facilitar el uso de la electrónica en proyectos multidisciplinares. Arduino es una plataforma abierta que facilita la programación de un microcontrolador.'
        ]
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
        print("    indexSimilarity")
        lenTokens = len(tokens)
        print("    "+str(lenTokens)+" tokens of  "+str(tokens))
        lenTokensSimilar = 0
        for tt in tokens:
            if tt in self.tokensInputs:
                lenTokensSimilar = lenTokensSimilar + 1
                print("    "+tt+" yes found ==> parcial: "+str(lenTokensSimilar))
            else:
                print("    "+tt+" not found ==> parcial: "+str(lenTokensSimilar))
        print("    indexSimilarity is "+str(lenTokensSimilar/lenTokens))
        return lenTokensSimilar/lenTokens

'''
Primermo evaluo si es necesario eliminar stopwords
Si se trata de una oración corta, no deberia ser tan necesario, ya que cada termino podría ser relevante, como es el caso de la pregunta
que es arduino. Un filtrado de stopwords eliminaria el es, dejando solo que, arduino algo que probablemente resulte muy dificil de evaluar
en la intención ya que la cantidad de valores a comparar es muy reducida.
Dependera mucho de la forma en que realize el motor de comparación.
'''

intent = CIntent()

'''
La estrategia es extraer de cada input probable los tokens mas importantes. Adjuntarlos en una lista simple donde cada token es irrepetible.
Una vez que adquiera la lista de tokens, me servira para que el motor de comparación pueda realizar su trabajo con la frase de entrada.
Quizas cada intent incluya parte del motor de comparación, es decir se ejecuta un metodo en el intent que dada una frase devuelve el % de
igualdad. A partir de dicho valor el motor de comparación deberá determinar cual intención es adecuada, en caso de indeterminación cedera
la decisión al motor de diferenciación que analizara el contexto
'''
tokens = []
print("analizando "+str(len(intent.inputs))+" inputs")
for i in intent.inputs:
    print("'"+i+"'")
    #extraigo las oraciones para evaluar la cantidad y determinar si debo filtrar stopwords o no
    sent = nltk.sent_tokenize(i,'spanish')
    tokens = nltk.word_tokenize(i, 'spanish')
    print("  "+str(len(sent))+" oraciones")
    print("  tokens>>"+str(tokens))
    if (len(sent) > 1):
        sw = stopwords.words('spanish')
        for token in tokens:
            if token in sw:
                tokens.remove(token)
    #ahora agrego a la lista de los tokens de la intención, las palabras que aun no estan precentes, independientemente de su uso
    '''
    otra forma podría ser juntar todos los inputs en un solo texto y trabajarlo desde allí,
    aunque quizas esto solo funcione si son todos los inputs frases cortas
    '''
    '''
    Para determinar que palabras deben ingresar y cuales no se puede analizar la distribución por frecuencias.
    Sin embargo, no sería del todo practico para frases cortas. En caso de frases largas, una forma eficaz de selección es distingir el 50%
    de una distribución cuyos valores estan elevados al cuadrado, de esta forma la distancia se extiende más.
    Sería el comportamiento inverso al buscado en otros algoritmos, donde importa la menor distancia de los cuadrados. En este caso 
    importa los elementos con mayor distancia... ¿50% o más?
    '''
    for token in tokens:
        if token not in intent.tokensInputs:
            intent.tokensInputs.append(token)
    '''
    la tokenización de palabras es lo que se espera, el problema pasa por los simbolos de puntuación. Por ejemplo, con la frase
    arduino, que es? se generan tokens individuales para la , y ?... estos signos son utiles para determinar la cantidad de las oraciones
    pero pueden generar ruido cuando se trata de comparar tokens para la intención
    no sería posible utilizar stopwords porque filtraria nuevamente palabras importantes en frases cortas. Lo unico q se me ocurre
    es evaluarlo manualmente... Esto pensando siempre en que sera todo por escrito.
    '''

print("tokens: ")
for t in intent.tokensInputs:
    print(t)
#hasta este punto ya obtuve todos los tokens necesarios para evaluar la entrada del usuario respecto a la entrada requerida para ejecutar la intención
#queda probar

print("---chat begin---")
text= input('>>')

#proceso la entrada para extraer la lista de tokens. Primero debo noramilaz
text = text.lower()
#deberia extraer acentos y quizas comas?
#genero el mismo procedimiento de tokenización que para los inputs de las intenciones
sent = nltk.sent_tokenize(text, 'spanish')
tokens = nltk.word_tokenize(text, 'spanish')
print("  "+str(len(sent))+" oraciones")
print("  tokens>>"+str(tokens))
if (len(sent) > 1):
    sw = stopwords.words('spanish')
    for token in tokens:
        if token in sw:
            tokens.remove(token)
#obteniendo los tokens de la entrada procedo a realizar la comparación... algoritmo de comparación
potencials = []
potencials.append( intent.indexSimilarity(tokens) )
if potencials[0]>0.5:
    print("ivy>>"+intent.outputs[0])
else:
    print("ivy>>?")
#ordeno por potenciales
'''
surge un problema,,, cuanta distancia se debe considerar para que una intención sea considerada sobresaliente por sobre otra?
si se toma el cubo del valor de coincidencia directa entonces es posible definir el 50%... siguiendo estos datos de prueba tenemos
[(1, 1),
 (0.9, 0.7290000000000001),
 (0.85, 0.6141249999999999),
 (0.8, 0.5120000000000001),
 (0.7, 0.3429999999999999),
 (0.6, 0.216),
 (0.59, 0.20537899999999998),
 (0.2, 0.008000000000000002),
 (0.1, 0.0010000000000000002)]

 vemos que los primeros 4 serían determinantes... el 1 implica coincidencia 100%, pero en caso de que no exista obtenemos una indeterminación
 Esto se puede resolver con otros metodos:
 analisis de contexto de conversación. Esto requeriria memoria a corto plazo.
 analisis de contexto de frecuencia. Esto requiere memoria a largo plazo y logica difusa
 dialogando con usuario para trabajar sobre las diferencias de las intenciones.
 En este ultimo caso, se debria quizas trabajar con la extracción de tokens diferenciados tanto en niveles de entradas como en niveles de salidas
 De esta forma se podría individualizar la frase e ir destacandola por sobre las otras con el mismo metodo usado para un primer acercamiento
 Esta estrategia ademas puede ser resuelta en futuras intervenciones registrando en una memoria de largo plazo.

 Por el momento deberia alcanzar con el cubo
'''


print("---chat end---")

if __name__ == "__main__":
    print("Ejecutado como Main")
