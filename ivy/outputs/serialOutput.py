# -*- coding: utf-8 -*-
import logging
import serial
from outputInterface import OutputInterface

class serialOutput(OutputInterface):
    def __init__(self, port="COM6", baudrate=9600, bytesize=serial.EIGHTBITS, parity=serial.PARITY_NONE,  \
                 stopbits=serial.STOPBITS_ONE, timeout=None, xonxoff=False, rtscts=False, dsrdtr=False, \
                 write_timeout=None, inter_byte_timeout=None):
        logging.debug("__init__ puerto serie")
        logging.debug("Conectando "+str(port))
        try:
            self.port = serial.Serial(port,baudrate,bytesize,parity,stopbits,timeout,xonxoff, rtscts, dsrdtr, write_timeout, inter_byte_timeout)
        except serial.SerialException:
            logging.error("serialOuput "+str(port)+" no se puede conectar")
            self.port = None
            self.success = False
            self.enable = False
        else:
            self.success = True
            self.enable = True

    def write(self,msg):
        if self.success:
            if self.enable:
                logging.debug("Enviando por "+str(self.port.port))
                try:
                    self.port.write(str(msg))
                except serial.SerialException:
                    logging.error("serialOuput "+str(self.port.port)+" no se puede enviar mensage")
