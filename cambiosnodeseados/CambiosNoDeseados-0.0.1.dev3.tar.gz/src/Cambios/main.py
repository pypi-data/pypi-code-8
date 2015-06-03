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
from Cambios.interfaz import Interfaz
from Cambios.reglas import Reglas, Jugador, crearPersonaje
from Cambios.juego import Juego, Mapa, Personaje
from Cambios.juego import Falta, PersonajeOcupado
from Cambios.cartas import Carta, MasoCartas, BuscarCarta


class CambiosNoDeseados(Process, Cliente, Interfaz):
    """Clase que la convinacion de la interfaz y el cliente"""

    PERSONAJES_PEDIDOS = []
    ESPERANDO_JUGADAS = False
    ACCIONES = []
    ACCION_ACTIVA = None

    juego = None
    jugador = None
    reglas = None

    def __init__(self, servidor='localhost', puerto=31425):
        Process.__init__(self, name='Cliente')
        Cliente.__init__(self, servidor, puerto)
        Interfaz.__init__(self)

    def run(self):
        while True:
            self.bucleRed()
            self.bucleGUI()
            self.Reloj.tick(self.FPS)

            self.verificarAccionActiva()

    def verificarAccionActiva(self):
        if self.ACCION_ACTIVA and self.ACCION_ACTIVA.listo():
            REG.debug('La Accion activa {} esta lista para enviarse'.format(self.ACCION_ACTIVA))
            self.ACCIONES.append(self.ACCION_ACTIVA)
            self.EnviarAccion(self.ACCION_ACTIVA)

            #~ try:
                #~ self.reglas.procesarJugadas(self.ACCION_ACTIVA)
            #~ except Falta as falta:
                #~ REG.warn('Accion {} no es valida debido a {}'.format(self.ACCION_ACTIVA, falta))
            #~ else:
                #~ self.ACCIONES.append(self.ACCION_ACTIVA)
                #~ self.EnviarAccion(self.ACCION_ACTIVA)

            self.ACCION_ACTIVA = None

    #Acciones de red
    def Network_PedirJugadas(self, datos):
        personajes = loads(datos['personajes'])
        self.PERSONAJES_PEDIDOS = personajes
        self.ESPERANDO_JUGADAS = True


def main():
    CambiosNoDeseados = CambiosNoDeseados()
    CambiosNoDeseados.start()

if __name__ == '__main__':
    main()
