#!/usr/bin/env python
# -*- coding: utf-8 -*-

from os import path
from logging import getLogger
from logging.config import fileConfig
CARPETA = path.abspath(path.dirname(__file__))
fileConfig(path.join(CARPETA, 'Logs', 'Cliente.conf'))
REG = getLogger('Main')

from multiprocessing import Process, get_logger
from pickle import dumps, loads
from time import sleep
from threading import Thread

from pygame import event
from pygame.locals import *

from Cambios.cliente import Cliente
from Cambios.servidor import Servidor



def main():
    pass

if __name__ == '__main__':
    main()
