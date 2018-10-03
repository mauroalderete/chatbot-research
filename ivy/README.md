# Ivy

Es un primer chatbot simple pensado para conversar sobre Arduino.

Esta desarrollado con libreria NLTK y posee su propio motor NLU.

Ivy mantiene similitudes con btty. Será diseñado para tratar temas de Arduino y tendra la capacidad para emitir diversos mensajes. El objetivo de este desarrolla es investigar e indagar sobre los procesos heuristicos de selección de intención ajustandome a los valores de entrada y estadisticas disponibles en la libreria NLTK.

> Aún no estoy seguro de si implementara la caracteristica de parafrasear su respuesta en función del feedback recibido, ya que involucraría algun nivel de memoria.

Más detalles en la bitacora de Ivy

## Bitacora

### 20181003-1700

Desarrolle un primer borrador de general del bot. Basicamente contiene un clase de intenciones que almacenan en su interior diferentes entradas posibles y salidas. El diseño se divide en tres etapas:

* 1-De *"aprendizaje"* donde se normalizan las entradas predefinidas del bot y se tokenizan.
* 2-Se normaliza y tokeniza el texto introducido por el usuario
* 3-Consiste en un motor de comparación. Se cuentan las cantidades de tokens coincidentes para todas las intenciones y se forma una lista de intenciones y su indice de similitud.
* 4-Se efectuan procesos para lograr alcanzar una sola intención
* 5-Se muestra la salida.

Hasta el momento ivy solo posee una sola intención, y el paso 4 consiste en un if indexSimilarity>0.5 then ok. Sin embargo, estoy analizando diferentes algoritmos de clasificación heuristicos que se podrían aplicar.

En la proxima version adaptare el codigo para que permita explotar multiples intenciones y configurar una forma de recibir el corpus inicial de alguna clase de script.

Dentro de los comentarios del codigo, que pasare a transcribir en este sitio, expongo algunas ideas y problemas que surgiran en la medida en que el bot sea cada vez más complejo. Incluso realizo algunas formas de implementar el uso de la memoria.

>'''
este dato servira mas adelante para la construcción de conversaciones sostenidas
la idea es que se enumeren los datos que son requeridos para satisfacer la intención
y si no estan satisfechos, entonces el motor de dialogo debera solicitar esos datos
Se podría construir como una lista (id, labels: ('','',''), regex=('##.#','*0','0?.*') )
'''
self.requiredEntities = [] 


>'''
Primermo evaluo si es necesario eliminar stopwords
Si se trata de una oración corta, no deberia ser tan necesario, ya que cada termino podría ser relevante, como es el caso de la pregunta
que es arduino. Un filtrado de stopwords eliminaria el es, dejando solo que, arduino algo que probablemente resulte muy dificil de evaluar
en la intención ya que la cantidad de valores a comparar es muy reducida.
Dependera mucho de la forma en que realize el motor de comparación.
'''

>'''
La estrategia es extraer de cada input probable los tokens mas importantes. Adjuntarlos en una lista simple donde cada token es irrepetible.
Una vez que adquiera la lista de tokens, me servira para que el motor de comparación pueda realizar su trabajo con la frase de entrada.
Quizas cada intent incluya parte del motor de comparación, es decir se ejecuta un metodo en el intent que dada una frase devuelve el % de
igualdad. A partir de dicho valor el motor de comparación deberá determinar cual intención es adecuada, en caso de indeterminación cedera
la decisión al motor de diferenciación que analizara el contexto
'''

>'''
ahora agrego a la lista de los tokens de la intención, las palabras que aun no estan precentes, independientemente de su uso
otra forma podría ser juntar todos los inputs en un solo texto y trabajarlo desde allí,
aunque quizas esto solo funcione si son todos los inputs frases cortas
'''

>'''
Para determinar que palabras deben ingresar y cuales no se puede analizar la distribución por frecuencias.
Sin embargo, no sería del todo practico para frases cortas. En caso de frases largas, una forma eficaz de selección es distingir el 50%
de una distribución cuyos valores estan elevados al cuadrado, de esta forma la distancia se extiende más.
Sería el comportamiento inverso al buscado en otros algoritmos, donde importa la menor distancia de los cuadrados. En este caso 
importa los elementos con mayor distancia... ¿50% o más?
'''

>'''
la tokenización de palabras es lo que se espera, el problema pasa por los simbolos de puntuación. Por ejemplo, con la frase
arduino, que es? se generan tokens individuales para la , y ?... estos signos son utiles para determinar la cantidad de las oraciones
pero pueden generar ruido cuando se trata de comparar tokens para la intención
no sería posible utilizar stopwords porque filtraria nuevamente palabras importantes en frases cortas. Lo unico q se me ocurre
es evaluarlo manualmente... Esto pensando siempre en que sera todo por escrito.
'''

>'''
ordeno por potenciales
surge un problema,,, cuanta distancia se debe considerar para que una intención sea considerada sobresaliente por sobre otra?
si se toma el cubo del valor de coincidencia directa entonces es posible definir el 50%... siguiendo estos datos de prueba tenemos

>>[(1, 1),
 (0.9, 0.7290000000000001),
 (0.85, 0.6141249999999999),
 (0.8, 0.5120000000000001),
 (0.7, 0.3429999999999999),
 (0.6, 0.216),
 (0.59, 0.20537899999999998),
 (0.2, 0.008000000000000002),
 (0.1, 0.0010000000000000002)]

 >vemos que los primeros 4 serían determinantes... el 1 implica coincidencia 100%, pero en caso de que no exista obtenemos una indeterminación
 Esto se puede resolver con otros metodos:
 analisis de contexto de conversación. Esto requeriria memoria a corto plazo.
 analisis de contexto de frecuencia. Esto requiere memoria a largo plazo y logica difusa
 dialogando con usuario para trabajar sobre las diferencias de las intenciones.
 En este ultimo caso, se debria quizas trabajar con la extracción de tokens diferenciados tanto en niveles de entradas como en niveles de salidas
 De esta forma se podría individualizar la frase e ir destacandola por sobre las otras con el mismo metodo usado para un primer acercamiento
 Esta estrategia ademas puede ser resuelta en futuras intervenciones registrando en una memoria de largo plazo.

 Por el momento deberia alcanzar con el cubo
'''

### 20181003-1800

Prepare el codigo para que se puedan generar varias intenciones. Aún es muy basico y rudimentario, pero lo importante es que es capaz de diferenciar las intenciones con un algoritmo simple de cantidad.

Obviamente faltan realizar muchas cosas más referente tanto a la arquitectura de datos, usabilidad, como a los algoritmos de los motores, division de clases y modulos... aún así es un gran progreso. Un progreso que no pude conseguir utilizando el chatterbot.

Por el momento las intenciones responden solo a tres casos:

* que es arduino
* donde comprar arduino
* que versiones existen de arduino

> me acabo de dar cuenta que no contemple los pluraes... quizas eso se pueda simplificar lemanizando¿?

En cualquier caso, la respuesta del programa presenta una salida de debbug que muestra la estructura reconocida del mensaje y el indice de similitud para cada intención. Luego muestra la salida.

Los valores mostrados para los indices de similitud son significativamente diferentes [1.0,0.3,0.6]. Esto depende directamente de la diferencia entre palabras que componen la frase de entrada (frase de activación) de cada intención. En todos los casos encontramos arduino, sin embargo palabras como es solo estan en la primer intención y palabras como comprar y existen en sus intenciones respectivas. Esto significa que el bot operara mucho mejor mientras las intenciones se encuentren bien diferenciadas y posean un mayor contenido. Pero, este contenido se traduce en frases largas que el usuario debe ingresar, cosa que incluso yo no haría.

