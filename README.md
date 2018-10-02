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