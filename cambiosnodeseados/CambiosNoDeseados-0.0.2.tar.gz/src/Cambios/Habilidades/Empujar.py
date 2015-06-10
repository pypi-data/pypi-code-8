#!/usr/bin/env python
# -*- coding: utf-8 -*-

from Cambios.juego import NoSuficientesRecursos, Pos
from Cambios.reglas import PERIODO
from Cambios.reglas import CAMPOSELECCIONADO

"""Efecto dañar 1"""

variables = {CAMPOSELECCIONADO:('objetivo',)}
duracion = PERIODO

costos = {'Agilidad':1}
extras = {'Rango':1}

def efecto(jugador, personaje, reglas, valores):
    inicio =  reglas.juego.mapa.buscar(personaje)
    final = valores['objetivo']
    var = Pos(1*(final.x-inicio.x), 1*(final.y-inicio.y))
    pos = final + var
    objetivo = reglas.juego.mapa[valores['objetivo']]
    objetivo = reglas.juego.buscarPersonaje(objetivo)

    try:
        if reglas.juego.mapa.buscarFondo(pos) in ('pared', 'esquina'):
            return
        if reglas.juego.mapa[pos]:
            return
        reglas.juego.mapa.mover(objetivo, pos)
    except KeyError:
        reglas.juego.mapa.quitar(final)
        objetivo.activo = False
