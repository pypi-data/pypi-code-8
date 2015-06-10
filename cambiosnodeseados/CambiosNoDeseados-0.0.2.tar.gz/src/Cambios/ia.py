#!/usr/bin/env python
# -*- coding: utf-8 -*-

from logging import getLogger
REG = getLogger('IA')


class IA():
    """Clase base para Inteligencias Artificiales"""

    def __call__(self, juego):
        pass


class Humano(IA):
    """Objeto que representa a un jugador humano"""

    def __call__(self, personaje, juego):
        return input('Jugada de {}: '.format(personaje.nombre))
