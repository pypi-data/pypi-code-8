#!/usr/bin/env python
# -*- coding: utf-8 -*-

from os import path
from logging import getLogger
from logging.config import fileConfig
CARPETA = path.abspath(path.dirname(__file__))
fileConfig(path.join(CARPETA, 'Logs', 'Cliente.conf'))
REG = getLogger('Cliente')

from multiprocessing import Process, get_logger
from time import sleep
from pickle import dumps, loads
from ConfigParser import ConfigParser, NoOptionError
from os import path
import sys

from PodSixNet.Connection import ConnectionListener, connection

from Cambios.interfaz import Interfaz
from Cambios.reglas import Reglas, Jugador, crearPersonaje
from Cambios.juego import Juego, Mapa, Personaje
from Cambios.juego import Falta, PersonajeOcupado
from Cambios.cartas import Carta, MasoCartas, BuscarCarta



CG = path.join(path.abspath(path.dirname(__file__)), 'Guardados')


class Cliente(Process, ConnectionListener, Interfaz):
    """Clase que la convinacion de la interfaz y el cliente"""

    PERSONAJES_PEDIDOS = []
    ESPERANDO_JUGADAS = False
    ACCIONES = []
    ACCION_ACTIVA = None

    juego = None
    jugador = None
    reglas = None

    def __init__(self, jugador, servidor='localhost', puerto=31425):
        Process.__init__(self, name='Cliente')
        Interfaz.__init__(self)
        self.Connect((servidor, puerto))
        REG.info("INICIANDO CONECCION A LOCALHOST")
        self.jugador = jugador

    def run(self):
        while True:
            self.bucleRed()
            self.bucleGUI()
            self.Reloj.tick(self.FPS)
            self.verificarAccionActiva()

    def bucleRed(self):
        connection.Pump()
        self.Pump()

    def verificarAccionActiva(self):
        if self.ACCION_ACTIVA and self.ACCION_ACTIVA.listo():
            REG.debug('La Accion activa {} esta lista para enviarse'.format(self.ACCION_ACTIVA))
            self.ACCIONES.append(self.ACCION_ACTIVA)
            self.EnviarAccion(self.ACCION_ACTIVA)
            self.ACCION_ACTIVA = None

    # Mensajes del Juego
    def EnviarAccion(self, accion):
        REG.info('Enviando la accion {} al Servidor'.format(accion))
        a = {
        'action' : 'RecivirAccion',
        'accion' : dumps(accion),
        }
        self.Send(a)

    # Llamas del juego
    def Network_ActualizarJuego(self, datos):
        self.reglas = loads(datos['reglas'])
        self.juego = self.reglas.juego
        self.jugador = self.reglas.jugadores[self.reglas.jugadores.index(self.jugador)]
        if datos['tipo'] == 'turno':
            #~ self.reglas.turno()
            REG.info('Turno {}'.format(self.juego.numeroTurno))
        if datos['tipo'] == 'periodo':
            #~ self.reglas.periodo()
            REG.info('Periodo {}'.format(self.juego.numeroPeriodo))
        if datos['tipo'] == 'terminado':
            REG.info('Juego Terminado, el ganador es {}'.format(self.reglas.terminado()))

    def Network_RecivirAccion(self, datos):
        accion = loads(datos['accion'])
        self.reglas.procesarJugadas(accion)
        self.ACCIONES.append(accion)

    def Network_PedirJugadas(self, datos):
        personajes = loads(datos['personajes'])
        self.PERSONAJES_PEDIDOS = personajes
        self.ESPERANDO_JUGADAS = True

    # Llamadas del sistema
    def Network_connected(self, datos):
        REG.info('Conectado con el servidor, enviando informacion personal')
        self.Send({
            'action':'EnviarJugador',
            'judador':dumps(self.jugador),
            })

    def Network_error(self, datos):
        REG.critical('error: {}'.format(datos['error']))
        connection.Close()

    def Network_disconnected(self, datps):
        REG.error('Server disconnected')



def cargarJugador(archivo):
    archivo = path.join(CG, '{}.conf'.format(archivo))
    conf = ConfigParser()
    conf.read(archivo)
    nombre_jugador = conf.get('Jugador', 'nombre')
    ps = conf.get('Jugador', 'personajes').split(',')
    maso = MasoCartas(10*len(ps))
    personajes = []
    for p in ps:
        sec = 'Personaje_{}'.format(p)
        personajes.append(BuscarCarta(int(conf.get(sec, 'codigo'))))
        maso.agregar(cargarMaso(conf, conf.get(sec, 'maso')))
    return Jugador(maso, personajes)


def cargarMaso(conf, seccion):
    maso = MasoCartas(10)
    seccion = 'Maso_{}'.format(seccion)
    cartas = []
    for n in range(10):
        try:
            c = conf.get(seccion, 'carta{}'.format(n))
            cartas.append(BuscarCarta(int(c)))
        except NoOptionError:
            cartas.append(None)
    maso.agregar(cartas)
    return maso


def inciarCliente(jugador, servidor, puerto):
    jugador = cargarJugador(jugador)
    cliente = Cliente(jugador, servidor, puerto)
    cliente.start()
    cliente.join()

def main():
    if len(sys.argv) != 3:
        print "Uso:", sys.argv[0], "Configuracion Conservidor:puerto"
        print "e.g.", sys.argv[0], "Config_1 localhost:31425"
    else:
        conf = sys.argv[1]
        host, port = sys.argv[2].split(":")
        inciarCliente(conf, host, int(port))

if __name__ == '__main__':
    main()
