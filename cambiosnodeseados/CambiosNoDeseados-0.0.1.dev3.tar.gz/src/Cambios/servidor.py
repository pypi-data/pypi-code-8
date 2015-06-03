#!/usr/bin/env python
# -*- coding: utf-8 -*-

from os import path
from logging import getLogger
from logging.config import fileConfig
CARPETA = path.abspath(path.dirname(__file__))
fileConfig(path.join(CARPETA, 'Logs', 'Servidor.conf'))
REG = getLogger('Servidor')

from multiprocessing import Process, get_logger
from threading import Thread
from time import sleep
from pickle import dumps, loads
from random import choice

from PodSixNet.Server import Server
from PodSixNet.Channel import Channel

from Cambios.reglas import Reglas, Jugador, crearPersonaje, cargarMapa
from Cambios.juego import Juego, Mapa, Personaje, Pos, Falta
from Cambios.cartas import Carta, MasoCartas, BuscarCarta


class Canal(Channel):

    def Network_EnviarJugador(self, datos):
        jugador = loads(datos['judador'])
        self.jugador = jugador

    def Network_RecivirAccion(self, datos):
        accion = loads(datos['accion'])
        REG.info('recibiendo jugadas de {}'.format(accion.personaje))
        try:
            self._server.reglas.procesarJugadas(accion)
        except Falta as err:
            REG.info('Accion invalida debido a {}'.format(err))
            self._server.enviarEstado(self)
        else:
            #~ self._server.RetransmitirAccion(self, accion)
            REG.info('Accion aceptada, transmitiendo a todos')
            self._server.TransmitirAccion(accion)
            REG.debug('accion transmitida')

    def Network_disconnected(self, datps):
        REG.info('Cliente {} se desconecto'.format(self.jugador))


class Servidor(Process, Server):

    channelClass = Canal

    def __init__(self, jugadoresMaximos=2, archivoMapa='Mapa1'):
        """Crea un Servidor en Localhost que espera hasta tener"""
        Process.__init__(self, name='Servidor')
        Server.__init__(self)
        self.jugadoresMaximos = jugadoresMaximos
        self.archivoMapa = archivoMapa
        self.canales = []

    def run(self):
        REG.info("INICIANDO EL SERVIDOR EN LOCALHOST")
        Thread(target=self.esperarJugadores).start()
        while True:
            self.buclePrincipal()

    def buclePrincipal(self):
        self.Pump()
        sleep(0.1)

    # Llamadas de Red
    def Connected(self, canal, direccion):
        if len(self.canales) < self.jugadoresMaximos:
            self.canales.append(canal)
            REG.info('Nuevo jugador {}, ya tenemos {} de {}'.format(canal, len(self.canales), self.jugadoresMaximos))
        else:
            canal.Send({
                'action':'error',
                'error': 'El Servidor esta lleno',
                })

    def enviarEstado(self, canal, tipo=''):
        REG.debug('Enviando estado forzado tipo {} a {}'.format(tipo, canal))
        canal.Send({
            'action':'ActualizarJuego',
            'reglas':dumps(self.reglas),
            'tipo':tipo,
            })

    def TransmitirTerminado(self, ganador):
        REG.info('Juego terminado, gano {}'.format(ganador))
        for canal in self.canales:
            self.enviarEstado(canal, 'terminado')

    def TransmitirTurno(self):
        REG.info('Turno {}'.format(self.juego.numeroTurno))
        for canal in self.canales:
            self.enviarEstado(canal, 'turno')

    def TransmitirPeriodo(self):
        REG.info('Periodo {}'.format(self.juego.numeroPeriodo))
        for canal in self.canales:
            self.enviarEstado(canal, 'periodo')

    def enviarAccion(self, canal, accion):
        canal.Send({
            'action':'RecivirAccion',
            'accion':dumps(accion),
            })

    def RetransmitirAccion(self, canalOrigen, accion):
        for canal in self.canales:
            if not canal is canalOrigen:
                self.enviarAccion(canal, accion)

    def TransmitirAccion(self, accion):
        for canal in self.canales:
            self.enviarAccion(canal, accion)

    def PedirJugadas(self, canal, personajes):
        if personajes:
            m = {
            'action':'PedirJugadas',
            'personajes':dumps(personajes),
            }
            canal.Send(m)


    # Prcesos del juego
    def esperarJugadores(self):
        while True:
            sleep(0.1)
            if len(self.canales) < self.jugadoresMaximos:
                continue
            for canal in self.canales:
                if not hasattr(canal, 'jugador'):
                    break
            else:
                break
        REG.info('Ya tenemos {} jugadores, iniciando el juego'.format(len(self.canales)))
        self.iniciarJuego()

    def iniciarJuego(self):
        self.cargarMapa()
        jugadores = [canal.jugador for canal in self.canales]
        personajes = []
        n = 0
        for jugador in jugadores:
            p = []
            for personaje in jugador.personajes:
                n = jugador.personajes.index(personaje)
                personaje = crearPersonaje(personaje)
                p.append(personaje)
                jugador.personajes[n] = hash(personaje)
                pos = choice([pos for pos, (fondo, objeto)
                    in self.mapa.items()
                    if objeto is None and fondo == 'piso'])
                self.mapa.colocar(personaje, pos)
            personajes.extend(p)
        self.juego = Juego(self.mapa, personajes)
        self.reglas = Reglas(self.juego, jugadores)

        while True:
            terminado = self.reglas.terminado()
            if terminado:
                self.TransmitirTerminado(terminado)
                break
            self.turno()

    def cargarMapa(self):
        if self.archivoMapa is None:
            mapa = []
            [mapa.extend(fila) for fila in [[(x, y) for x in range(8)] for y in range(8)]]
            mapa = Mapa(mapa)
            for pos, objeto in mapa.items():
                mapa.colocar('piso', pos)
        else:
            archivo = path.join(
                path.abspath(path.dirname(__file__)), 'Mapas', self.archivoMapa)
            mapa = cargarMapa(archivo)
        self.mapa = mapa

    # cliclo de juego
    def turno(self):
        self.reglas.turno()
        periodo = self.reglas.personajesTurno()
        self.TransmitirTurno()
        for personajes in periodo:
            self.periodo(personajes)

    def periodo(self, personajes):
        self.reglas.periodo()
        personajes = self.reglas.personajesPeriodo(personajes)
        self.TransmitirPeriodo()
        for canal in self.canales:
            p = []
            for personaje in personajes:
                if personaje in canal.jugador.personajes:
                    p.append(personaje)
            self.PedirJugadas(canal, p)
        while not self.reglas.periodoTerminado():
            sleep(0.05)
        REG.info('Todos los personjes requeridos tomaron sus acciones')


def main():
    servidor = Servidor(2, 'Mapa1')
    servidor.start()


if __name__ == '__main__':
    main()
