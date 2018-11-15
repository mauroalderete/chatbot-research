# -*- coding: utf-8 -*-
import logging
import serial
from outputInterface import OutputInterface

class standarOutput(OutputInterface):
    def __init__(self,header="Sending::",footer=""):
        logging.debug("__init__ consola")
        self.header = header
        self. footer = footer
        self.success=True
        self.enable=True
    def write(self,msg):
        logging.debug("write consola")
        print(str(self.header)+str(msg)+str(self.footer))
