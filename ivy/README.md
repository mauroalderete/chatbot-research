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

### 20181005-0130

Traslade la clase de intenciones a su propio modulo. Tambien cree un metodo para que aprenda y carge los inputs y outputs necesarios. De esta forma al crear una clase sería posible pasarle las listas de inputs y outputs inmediatamente, luego procede a normalizarlas y extraer los tokens necesarios.

Al final lo unico que queda por realizar cada vez que el usuario ingresa una entrada es procesarla y consultar con el metodo indexSimilarity para extraer el indice de similaridad.

Realice una prueba y note que sería posible, en caso de incertidumbre, brindar sugerencias de temas. Esto nuevamente requiere de memoria, pero al mismo tiempo requiere de la articulación predefinida de esa sugerencia. Por ejemplo ivy podría decir: *usted desea saber donde comprar un arduino?* cuando el indice de incertidumbre no es suficiente para destacar una sentencia. 

Otras variantes sobre ese metodo podrían ser:

* Sugerir mas de una posible intención
* En caso de que halla seleccionado la intención, almacenar la entrada como un nuevo input (tokenizandola como toda entrada).
* Asignar a la nueva entrada un indice de probabilidad. En la medida en que vuelva a citar tokens que se encuentran en la nueva entrada y no esten en las siguientes, y la intención haya sido evaluada correctamente esta probabilidad aumentaria. Se logra un refuerzo de un nuevo conocimiento.

Voy a añadir algunas intenciones más. Por el momento no actualize el metodo para generar las intenciones y las respuestas. Debo investigar los formatos preexistentes. Quizas utilize un json o el simple yml, aunque este ultimo no le veo capacidad para discriminar entradas. Otra posibilidad seria una  o pequeña base de datos litesql o quizas una base de documentos tipo la de google, con lo que luego deberia ser más facil migrar.

Otras cosas que quisiera ir explorando son el uso del script como un servidor y la creación de una GUI con python. En el caso de la primera quizas sea un programa cliente de la base de datos de google que esta atenta a nuevas solicitudes.

### 20181005-215

Agrege unos intents, trate de ser variado y sobre cada variación ofrecer dos o tres intents similares. Los resultados son bastante interesantes. Nuevamente surge la necesidad de encontrar una tecnica para la resolución de incertidumbre.

Incertidumbre en dos sentidos, tanto cuando los indices de similitud son muy bajos, como cuando existen muchos candidatos posibles.

Otro incidente que observe es que hay terminos que se aplican mucho, como pueden ser "Arduino"... Esto me hace pensar, que sucederia si niego ese termino en todos los intents... la performance se mantiene? Y si lo niego solo en algunos?

Algunas estrategias para resolver la incertidumbre donde existen muchos candidatos puede ser:

* tokenizar la salida y revisar las coincidencias desde allí.
* Descartar aquellos intents que fueron consultados recientemente. Se podría colocar un indice de intent ejecutado, de manera tal que cuando exista una colisión de candidatura, los que tengan mayor indice de ejecución reciente deberían ser menos probable que se ejecute nuevamente. Dicho indice podría disminuir con cada intent que no es el suyo, por tiempo real u otro factor.

Esto significa que mucho del codigo del motor de selección se trataría de diversos indices probabilisticos. Sería interesante verlo como un sistema de calificación con ELO. Algo así como un ELO para cada entrada X. Al final de cuenta se trata de evaluar que intención es la mejor para satisfacer una entrada.

### 20181027-2200

Realizando una revisión de las notas pienso algunas alternatvas para seguir trabajando el codigo:
* Variar el objetivo del chatbot a uno orientado a la asistencia
* Cuando se genera una incertidumbre de una intención, la misma intención almacena la forma gramatical para sugerir su entrada
* Las entradas del usuario pueden ser almacenados y relacionados con la intención dada.
> Esto plantea dos situaciones. Por un lado no hay una forma certera de asegurar que la intención seleccionada responda correctamente a la entrada dada por el usuario, por lo que la relación puede ser equivocada. Fenonemo que sucede en el chatterbot. Por el contrario, cuando existe una situación de incertidumbre y el bot responde con una sugerencia de intención que luego el usuario confirma, se obtiene un feedback positivo que permite relacionar fuertemente la entrada dada originalmente con la intención ejecutada. En este caso se podría tratar de tokenizar la entrada para reforzar el indice de similiridad.
* Las conversaciones pueden responder a una maquina oculta, HHM. Sin embargo existen complicaciones para definir fronteras, es decir, para determinar cuando entra en una HHM correspondiente a una serie de intenciones, cuando debe finalizarla, o cuando debe pausarlas y retomarlas. Al mismo tiempo requiere de un variables de estado que sean capaces de manejar los distintos hilos de conversasion.
* La primer función buscada del asistente debe ser el de agenda. Deberá ser capaz de almacenar recordatorios con fechas, horas, repitencia, pero tambien con metodos más relativos que respondan a frases como "más tarde", "en un rato", "por la noche", "despues de <acción>"

Por otra parte voy a preparar un fork del proyecto en la forma tal y como esta hasta el momento para el un curso de robotica. El fork consistira en un chatbot conversacional abierto que se conectara a un robot con arduino por medio de la comunicación en serie y respondera utilizando un display LCD.

### 20181101-2300

Comence a realizar algunas de las modificaciones anunciadas.
* Trabaje sobre los sistemas de salidas.
* Intento construir un formato json para almacenar las intenciones y los tokens
* Preparo el codigo pensando en el taller

Cree unas clases que permiten seleccionar las distintas fuentes de salida del mensaje del chatbot. Por el momento solo hay dos, la salida por pantalla estandar y la salida por puerto serial, que aun falta probar. La idea es implementar mas tipos de salidas para conexiones a base de datos, aplicaciones blutooth, etc...
Las salidas implementan una interface que luego es heredada por las salidas estandar. Aplicando polimorfismo sobre un administrador de salidas, este ejecuta los metodos estandar de cada clase de salida en particular
Esta forma de estructurar los sistemas de salidas, es extensible tanto en horizontal como en vertical.

Algo similar quize implementar con las intenciones. Una clase de intensiones y otra para administrarlas.

Por otro lado cree un archivo JSON para estructurar los datos de las intenciones y los tokens. Una clave checksum para verificar si es necesaria una actualización de los tokens o se pueden usar los que ya estan disponibles.

Al final, cuando se realiza toda la carga, el sistema tokeniza lo que es necesario y deja todo listo para analizar las frases. En este punto se puede realizar una actualización del corpus. Sin embargo, esto genera complicaciones con las codificaciones de caracteres.