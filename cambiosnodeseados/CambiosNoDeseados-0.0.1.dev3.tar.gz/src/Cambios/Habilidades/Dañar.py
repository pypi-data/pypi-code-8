#!/usr/bin/env python
# -*- coding: utf-8 -*-

from Cambios.reglas import Falta, NoSuficientesRecursos
from Cambios.reglas import NADA, PERIODO, TURNO
from Cambios.reglas import CAMPOSELECCIONADO, COMANDOSELECCIONADO, CARTASELECCIONADA

"""Efecto dañar 1"""

variables = {CAMPOSELECCIONADO:('objetivo',)}
duracion = PERIODO

costos = {'Resistencia':1}
extras = {}

def efecto(reglas, valores):
    objetivo = reglas.juego.mapa[valores['objetivo']]
    if objetivo:
        personaje = reglas.juego.buscarPersonaje(objetivo)
        try:
            personaje.destruirRecursos('Resistencia', 1)
        except NoSuficientesRecursos:
            personaje.activo = False
