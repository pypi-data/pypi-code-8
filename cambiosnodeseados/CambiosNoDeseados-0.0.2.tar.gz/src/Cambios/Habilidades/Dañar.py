#!/usr/bin/env python
# -*- coding: utf-8 -*-

from Cambios.juego import NoSuficientesRecursos
from Cambios.reglas import PERIODO
from Cambios.reglas import CAMPOSELECCIONADO

"""Efecto dañar 1"""

variables = {CAMPOSELECCIONADO:('objetivo',)}
duracion = PERIODO

costos = {'Resistencia':1}
extras = {'Rango':1}

def efecto(jugador, personaje, reglas, valores):
    objetivo = reglas.juego.mapa[valores['objetivo']]
    personaje = reglas.juego.buscarPersonaje(objetivo)
    try:
        personaje.destruirRecursos('Resistencia', 1)
    except AttributeError:
        pass
    except NoSuficientesRecursos:
        personaje.activo = False
