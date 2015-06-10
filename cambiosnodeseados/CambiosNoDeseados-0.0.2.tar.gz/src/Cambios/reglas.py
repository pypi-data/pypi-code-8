#!/usr/bin/env python
# -*- coding: utf-8 -*-

from logging import getLogger
REG = getLogger('Reglas')

from ast import literal_eval
from uuid import uuid4
from importlib import import_module

from Cambios.juego import Juego, Mapa, Personaje, Pos
from Cambios.juego import Falta, PersonajeOcupado, LimiteReacurso, NoSuficientesRecursos, NoSuficienteRango
from Cambios.cartas import BuscarCarta, Carta, MasoCartas
import Cambios.Habilidades


MAPEO_ICONOS = {
    '+': 'esquina',
    '@': 'pared',
    '.': 'piso',
    '_': 'grama',
    ' ': None,
    }

NADA = bin(0)
PERIODO = bin(1)
TURNO = bin(2)

CAMPOSELECCIONADO = 25
COMANDOSELECCIONADO = 26
CARTASELECCIONADA = 27


class Reglas(object):
    """Clase principal, mantiene las reglas"""

    def __init__(self, juego, jugadores):
        self.juego = juego
        self.jugadores = jugadores

    def turno(self):
        self.juego._turno += 1
        for jugador in self.jugadores:
            jugador.tomarCartas()
        for personaje in self.juego.personajes:
            for carta in personaje.recursos:
                carta.activa = True
            personaje.carta.activa = True

    def periodo(self):
        pass

    def jugadoresActivos(self):
        jugadores = []
        for jugador in self.jugadores:
            personajes = []
            for personaje in jugador.personajes:
                personaje = self.juego.buscarPersonaje(personaje)
                if personaje:
                    personajes.append(personaje)
            if personajes:
                jugadores.append(jugador)
        return jugadores

    def terminado(self):
        jugadores = self.jugadoresActivos()
        if len(jugadores) == 1:
            return jugadores[0]
        else:
            return False

    def personajesTurno(self):
        self.ocupaciones = {}
        for personaje in [hash(p) for p in self.juego.personajes]:
            self.ocupaciones[personaje] = NADA
        return self.juego.listaPersonajes

    def personajesPeriodo(self, personajes):
        self.personajesRequeridos = []
        for personaje in [hash(personaje) for personaje in personajes]:
            if self.ocupaciones[personaje] == PERIODO:
                self.ocupaciones[personaje] = NADA
            if self.ocupaciones[personaje] == NADA:
                self.personajesRequeridos.append(personaje)
        return self.personajesRequeridos

    def periodoTerminado(self):
        for personaje in self.personajesRequeridos:
            if (self.ocupaciones[personaje] == NADA and
                self.juego.buscarPersonaje(personaje).activo):
                return False
        return True

    @property
    def personajesOcupados(self):
        personajes = []
        for personaje in [hash(p) for p in self.juego.personajes]:
            if not self.ocupaciones[personaje] == NADA:
                personajes.append(personaje)
        return personajes

    def procesarJugadas(self, accion):
        REG.info('{} tomo accion {}'.format(accion.personaje, accion))

        if self.ocupaciones[accion.personaje] in (PERIODO, TURNO):
            raise PersonajeOcupado('{} esta en estado {}'.format(accion.personaje, self.ocupaciones[accion.personaje]))
        elif accion.tipo in ('esperar', 'movimiento', 'acoplar', 'habilidad'):
            REG.debug('{} ahora tiene in nivel de ocupacion {}'.format(accion.personaje, accion.duracion))
            self.ocupaciones[accion.personaje] = accion.duracion

        if accion.tipo == 'esperar':
            pass

        elif accion.tipo == 'movimiento':
            self.procesarMovimiento(accion)

        elif accion.tipo == 'acoplar':
            self.procesarAcoplar(accion)

        elif accion.tipo == 'habilidad':
            accion(self)

    def procesarAcoplar(self, accion):
        for jugador in self.jugadores:
            for p in [self.juego.buscarPersonaje(p) for p in jugador.personajes]:
                if hash(p) == accion.personaje and accion['carta'].tipo == 'Recurso':
                    if p.resistencia > 0:
                        p.acoplar(accion['carta'])
                        del jugador.mano[accion['pos']]
                        p.desactivarRecursos('Resistencia')
                    elif p.resistencia == 0 and p.carta.activa:
                        p.acoplar(accion['carta'])
                        del jugador.mano[accion['pos']]
                        p.carta.activa = False
                    else:
                        raise NoSuficientesRecursos('{} no tiene suficientes Resistencia'.format(p))
                elif hash(p) == accion.personaje and accion['carta'].tipo == 'Habilidad':
                    p.acoplar(accion['carta'])
                    del jugador.mano[accion['pos']]

    def procesarMovimiento(self, accion):
        p = self.juego.mapa.buscar(accion.personaje)
        personaje = self.juego.buscarPersonaje(accion.personaje)
        REG.debug('Procesando accion moviemietno con objetivo {}'.format(accion['objetivo']))
        if accion['objetivo'] is None:
            raise Falta('Debes Seleccionar un cuadro')
        elif accion['objetivo'] not in (Pos(p.x+1,p.y),Pos(p.x-1,p.y),Pos(p.x,p.y+1),Pos(p.x,p.y-1)):
            raise Falta('Solo se puede mover un cuadro a la ves')
        elif (self.juego.mapa.buscarFondo(accion['objetivo']) not in ('grama', 'piso')):
            raise Falta('Solo te puedes mover al piso o la grama')
        elif not self.juego.mapa[accion['objetivo']] is None:
            raise Falta('Ese Cuadro ya esta ocupado')

        if personaje.agilidad > 0:
            self.juego.mapa.mover(accion.personaje, accion['objetivo'])
            personaje.desactivarRecursos('Agilidad')
        elif personaje.agilidad == 0 and personaje.carta.activa:
            self.juego.mapa.mover(accion.personaje, accion['objetivo'])
            personaje.carta.activa = False
        else:
            raise NoSuficientesRecursos('{} no tiene suficientes Agilidad'.format(personaje))


class Jugador(object):
    """Clase base para los Jugadores"""

    def __init__(self, maso, personajes):
        self.maso = maso
        self.mano = []
        self.personajes = list(personajes)
        self._uuid = int(uuid4())

    def tomarCartas(self):
        cartas = self.maso.tomar(2*len(self.personajes))
        c = []
        for carta in cartas:
            if not carta is None:
                c.append(carta)
        self.mano.extend(c)

    def __hash__(self):
        return self._uuid

    def __eq__(self, objeto):
        if type(objeto) is type(self):
            if hash(objeto) == hash(self):
                return True
            else:
                return False
        else:
            return NotImplemented


class Accion(object):
    """Objeto que representa una accion que un personaje realiza"""

    def __init__(self, tipo, duracion, personaje, variables={}):
        """tipo: 'TipoDeAccion', duracion: 'NADA|PERIODO|TURNO',variables: {TIPOEVENTO:('valorDeseado1','valorDesaeo2')}"""
        self.tipo == tipo
        self.duracion = duracion
        self.personaje = personaje
        self.variables = variables
        self.valores = {}

    def agregarVariable(self, evento):
        if evento.type == CAMPOSELECCIONADO:
            if not evento.objetivo is None:
                REG.debug('Agegando el objetivo pos {}'.format(evento.objetivo))
                self.valores['objetivo'] = evento.objetivo
        elif evento.type == CARTASELECCIONADA:
            if not (evento.carta is None or evento.pos is None):
                self.valores['carta'] = evento.carta
                self.valores['pos'] = evento.pos

    def listo(self):
        l = True
        for tipo, variables in self.variables.items():
            for variable in variables:
                if not variable in self.valores:
                    l = False
        return l

    def __getitem__(self, llave):
        return self.valores[llave]

class Esperar(Accion):
    """Subclase de Accion especifica del comando esperar"""

    tipo = 'esperar'
    duracion = PERIODO

    def __init__(self, personaje):
        self.personaje = personaje
        self.variables = {}
        self.valores = {}

class Movimiento(Accion):
    """Subclase de Accion especifica del comando moverse"""

    tipo = 'movimiento'
    duracion = NADA

    def __init__(self, personaje):
        self.personaje = personaje
        self.variables = {CAMPOSELECCIONADO:('objetivo',)}
        self.valores = {}

class Acoplar(Accion):
    """Subclase de Accion especifica del comando acoplar carta"""

    tipo = 'acoplar'
    duracion = NADA

    def __init__(self, personaje):
        self.personaje = personaje
        self.variables = {CARTASELECCIONADA:('carta', 'pos')}
        self.valores = {}

class Habilidad(Accion):
    """Subclase de Accion genreal para las habilidades de carta"""

    tipo = 'habilidad'

    def __init__(self, jugador, personaje, habilidad):
        REG.debug('Ejecutando comando <{habilidad}> del personaje {personaje} de {jugador}'.format(**locals()))
        self.jugador = jugador
        self.personaje = personaje
        self.habilidad = habilidad
        habilidad = import_module('.'+habilidad, package='Cambios.Habilidades')
        self.efecto = habilidad.efecto
        self.variables = habilidad.variables
        self.duracion = habilidad.duracion
        self.costos = habilidad.costos
        self.extras = habilidad.extras
        self.valores = {}

    def verificarCostos(self, reglas):
        personaje = reglas.juego.buscarPersonaje(self.personaje)
        for costo in self.costos:
            if personaje.obtenerAtributo(costo) < self.costos[costo]:
                return False
        else:
            return True

    def verificarExtras(self, reglas):
        for extra in self.extras:
            if extra == 'Rango':
                origen = reglas.juego.mapa.buscar(self.personaje)
                if int(origen-self.valores['objetivo']) > self.extras[extra]:
                    return False
        else:
            return True

    def cobrarCostos(self, reglas):
        personaje = reglas.juego.buscarPersonaje(self.personaje)
        jugador = [jugador for jugador in reglas.jugadores if self.personaje in jugador.personajes][0]
        for costo in self.costos:
            REG.debug('Cobrando {}{} a {}'.format(self.costos[costo], costo, self.personaje))
            cartas = personaje.destruirRecursos(costo, self.costos[costo])
            jugador.maso.agregar(cartas)

    def __call__(self, reglas):
        REG.debug('Usando habilidad {}'.format(self.habilidad))
        if not self.verificarCostos(reglas):
            raise NoSuficientesRecursos('Personaje {} no tiene suficientes recursos'.format(self.personaje))
        if not self.verificarExtras(reglas):
            raise NoSuficienteRango('Esa habilidad no puede ser usada de esa forma')
        self.cobrarCostos(reglas)
        self.efecto(self.jugador, self.personaje, reglas, self.valores)


def crearPersonaje(carta, nombre=None):
    """Crea un objeto juego.Personaje apratir de un objeto cartas.Carta"""
    if issubclass(type(carta), Carta) and carta.tipo == 'Personaje':
        p = Personaje(nombre if nombre else carta.nombre,
            carta.salud,
            carta.consentracion,
            carta.movilidad,
            carta.efecto,
            carta.imagen.archivo,
            carta)
        return p
    else:
        raise TypeError('Se necesita un objeto Carta de tipo Personaje')


def cargarMapa(archivo):
    posiciones = {}
    with open(archivo) as archivo:
        lineas = archivo.readlines()
    for y in range(len(lineas)):
        lineas[y] = lineas[y][:-1]
        if lineas[y][0] == '#':
            continue
        for x in range(len(lineas[y])):
            icono = MAPEO_ICONOS[lineas[y][x]]
            if icono is None:
                continue
            else:
                posiciones[(x,y)] = icono
    mapa = Mapa([p for p in posiciones])
    for p in posiciones:
        mapa.agregarFondo(posiciones[p], p)
    return mapa
