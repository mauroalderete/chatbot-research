# Proyecto Chatbot 

Se trata de una serie de desarrollos orientados a implementar en un chatbot diferentes estrategias del campo de la IA previos a la implementación masiva de las redes neuronales.
Se busca estudiar, practicar y experimentar, entre otras opciones, con:

* árbol de decisiones
* logica difusa
* procesamiento de lenguaje natural
* reconocimiento de voz
* sintesis de voz

## btty

Se trata del primer intento de chatbot utilizando la libreria chatterbot. El objetivo era crear un asistente para responder a dudas sobre Arduino. El chatbot sería capaz de recibir un feedback por parte del usario sobre la comprension del tema y ofrecer nuevas respuestas predefinidas. Al final en caso de que el usuario siga sin comprender lo motivaba a consultar al docente.

Más alla de la ineficiente construcción de las ramas de conversación, resutló que la libreria carecia de memoria, es decir, no era capaz de mantener una rama de conversación en función de las respuestas pasadas. Esto, sumado a que la libreria estaba construida de tal forma que su aprendizaje carecia de criterios optimos para establecer un feedback de su performance,  provocó que se desestime la libreria por completo.

Más detalles en la sección de bitacoras con fecha 20181002-1545

## ivy

Se trata de un chatbot simple, sin memoria, utilizando la poplar libreria NLTK. El objetivo es crear un motor NLU simple implementando las funciones de la libreria NLTK.

Ivy mantiene similitudes con btty. Será diseñado para tratar temas de Arduino y tendra la capacidad para emitir diversos mensajes. El objetivo de este desarrolla es investigar e indagar sobre los procesos heuristicos de selección de intención ajustandome a los valores de entrada y estadisticas disponibles en la libreria NLTK.

> Aún no estoy seguro de si implementara la caracteristica de parafrasear su respuesta en función del feedback recibido, ya que involucraría algun nivel de memoria.

Más detalles en la bitacora de Ivy