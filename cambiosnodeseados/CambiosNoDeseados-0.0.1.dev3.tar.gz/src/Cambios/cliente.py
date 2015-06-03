#!/usr/bin/env python
# -*- coding: utf-8 -*-

from logging import getLogger
REG = getLogger('Cliente')

from time import sleep
from pickle import dumps, loads
import sys

from PodSixNet.Connection import ConnectionListener, connection

from Cambios.reglas import Reglas, Jugador, crearPersonaje
from Cambios.juego import Juego, Mapa, Personaje
from Cambios.cartas import Carta, MasoCartas, BuscarCarta


class Cliente(ConnectionListener):

    def __init__(self, servidor, puerto):
        self.Connect((servidor, puerto))
        REG.info("INICIANDO CONECCION A LOCALHOST")

    def bucleRed(self):
        connection.Pump()
        self.Pump()

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


def main():
    # Informacion del juego preconf
    personajes = [100000401, 100000501, 100000601, 100000701]
    recursos = [100000201, 100000101, 100000301]
    habilidades = [100000801, 100000901, 100001001]
    cartas = [
        BuscarCarta(recursos[0]),
        BuscarCarta(recursos[0]),
        BuscarCarta(recursos[0]),
        BuscarCarta(recursos[1]),
        BuscarCarta(recursos[1]),
        BuscarCarta(recursos[2]),
        BuscarCarta(recursos[2]),
        BuscarCarta(habilidades[0]),
        BuscarCarta(habilidades[1]),
        BuscarCarta(habilidades[2]),
        ]
    maso = MasoCartas(10)
    maso.agregar(cartas)
    jugador = Jugador(maso, (BuscarCarta(personajes[0]), BuscarCarta(personajes[1])))

    # Incio del cliente
    c = Cliente()
    c.start()


if __name__ == '__main__':
    main()
