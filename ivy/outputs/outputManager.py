# -*- coding: utf-8 -*-
import logging
import serial
from outputInterface import OutputInterface

class OutputManager( OutputInterface ):
    outs = []
    def __init__(self):
        logging.debug("__init__ Administrador de Salidas")
    def loadOuput(self, outp ):
        logging.debug("__init__ Cargando una nueva salida")
        self.outs.append( outp )
    def write(self,msg):
        logging.debug("Escribiendo en las salidas")
        for o in self.outs:
            if o.success:
                if o.enable:
                    o.write(msg)
