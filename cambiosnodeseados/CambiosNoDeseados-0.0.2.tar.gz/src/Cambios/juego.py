#!/usr/bin/env python
# -*- coding: utf-8 -*-

from logging import getLogger
REG = getLogger('Juego')

from uuid import uuid4
from os import path

from pygame import image, transform


CA = path.join(path.abspath(path.dirname(__file__)), 'Arte')


class Falta(Exception):
    """Error base para faltas de las reglas del juego"""
    pass

class LimiteReacurso(Falta):
    """Limite de recursos de un tipo alcansado"""
    pass

class NoSuficientesRecursos(Falta):
    """No hay suficientes recursos de un tipo"""
    pass

class PersonajeOcupado(Falta):
    """Personaje esta ocupado"""
    pass

class NoSuficienteRango(Falta):
    """La distancia es mayor que el Rango permitido"""
    pass


class Juego(object):
    """Clase principal del Juego, interfaz por donde controlar todos los componentes"""

    _turno = 0

    def __init__(self, mapa, personajes):
        self.mapa = mapa
        self.listaPersonajes = listaPersonajes(personajes)

    def buscarPersonaje(self, codigo):
        for personaje in self.personajes:
            if hash(personaje) == codigo:
                return personaje
        else:
            return None

    @property
    def personajes(self):
        return self.listaPersonajes.personajes

    @property
    def personajesActivos(self):
        return self.listaPersonajes.personajesActivos

    @property
    def numeroTurno(self):
        return self._turno

    @property
    def numeroPeriodo(self):
        return self.listaPersonajes.nivel + 1


class Mapa(dict):
    """Clase base para mapas"""

    def __init__(self, posiciones):
        """Crea un mapa cuyos pociciones sean las especificadas"""
        dict.__init__(self)
        for pos in posiciones:
            p = Pos(pos[0], pos[1])
            dict.__setitem__(self, p, [None, None])

    def __getitem__(self, llave):
        if type(llave) is Pos:
            return dict.__getitem__(self, llave)[1]
        else:
            raise TypeError('La llave debe se de tipo Pos')

    def __setitem__(self, llave, valor):
        if type(llave) is Pos:
            dict.__getitem__(self, llave)[1] = valor
        else:
            raise TypeError('La llave debe se de tipo Pos')

    def lista(self):
        """Regresa los contenidos del mapa como una lista ordenada"""
        lista = []
        for x in range(self.totX):
            columna = []
            for y in range(self.totY):
                columna.append(None)
            lista.append(columna)
        for pos, objeto in self.items():
            lista[pos.x][pos.y] = (pos, objeto)
        r = []
        for x in lista:
            for y in x:
                if y:
                    r.append(y)
        return r

    @property
    def totX(self):
        return max([pos.x for pos, objeto in self.items()]) + 1

    @property
    def totY(self):
        return max([pos.y for pos, objeto in self.items()]) + 1

    def __str__(self):
        s = 'Mapa\n----------------------------------------------------'
        for pos, objeto in self.items():
            if objeto:
                s += '\n{}:{}'.format(objeto[1], pos)
        return s

    def buscar(self, personaje):
        """busca por toda las ubicaciones a un objeto"""
        for pos, (f, p) in self.items():
            if hash(personaje) == p:
                return pos
        else:
            raise KeyError('No se encontro el personaje dentro del mapa')

    def colocar(self, personaje, pos):
        p = Pos(pos[0], pos[1]) if not type(pos) is Pos else pos
        self[p] = hash(personaje)

    def quitar(self, pos):
        p = Pos(pos[0], pos[1]) if not type(pos) is Pos else pos
        self[p] = None

    def mover(self, personaje, pos):
        p = Pos(pos[0], pos[1]) if not type(pos) is Pos else pos
        llave = self.buscar(personaje)
        self.quitar(llave)
        self.colocar(personaje, p)

    def buscarFondo(self, pos):
        p = Pos(pos[0], pos[1]) if not type(pos) is Pos else pos
        return dict.__getitem__(self, p)[0]

    def agregarFondo(self, fondo, pos):
        p = Pos(pos[0], pos[1]) if not type(pos) is Pos else pos
        dict.__getitem__(self, p)[0] = fondo


class Personaje(object):
    """Clase base para personajes"""

    _imagen = None
    activo = True

    def __init__(self, nombre, resistencia=0, energia=0, agilidad=0, efecto=None, arte=None, carta=None):
        self.nombre = nombre
        self._uuid = int(uuid4())

        self._resistencia = resistencia
        self._energia = energia
        self._agilidad = agilidad

        self.efecto = efecto
        self.recursos = []
        self.habilidades = []

        self.arte = arte
        self.carta = carta

    def acoplar(self, carta):
        mapeo_max = {
            'Resistencia':self._resistencia,
            'Energia':self._energia,
            'Agilidad':self._agilidad}
        mapeo_peso = {
            'Resistencia':self.pesoResistencia,
            'Energia':self.pesoEnergia,
            'Agilidad':self.pesoAgilidad}
        if carta.tipo == 'Recurso':
            maximo = mapeo_max[carta.subtipo]
            peso = mapeo_peso[carta.subtipo] + carta.peso
            if peso <= maximo:
                self.recursos.append(carta)
            else:
                raise LimiteReacurso('El personaje a alcansado el limite de {} equipable'.format(carta.subtipo))
        elif carta.tipo == 'Habilidad':
            self.habilidades.append(carta)

    def desactivarRecursos(self, tipo, cantidad=1):
        cantidad = abs(cantidad)
        n = 0
        for carta in self.recursos:
            if carta.subtipo == tipo and carta.activa:
                carta.activa = False
                n += carta.valor
            if n >= cantidad:
                break
        else:
            raise NoSuficientesRecursos('{} no tiene {} {}'.format(self.nombre, cantidad, tipo))

    def destruirRecursos(self, tipo, cantidad=1):
        REG.debug('Destruyendo {} {} de {}'.format(cantidad, tipo, self))
        cantidad = abs(cantidad)
        n = 0
        cartas = []
        for carta in self.recursos:
            if carta.subtipo == tipo:
                cartas.append(carta)
                n += carta.valor
            if n >= cantidad:
                break
        else:
            raise NoSuficientesRecursos('{} no tiene {} {}'.format(self.nombre, cantidad, tipo))
        for carta in cartas:
            del self.recursos[self.recursos.index(carta)]
        return cartas

    def obtenerAtributo(self, atributo):
        if atributo == 'Resistencia':
            return self.resistencia
        if atributo == 'Energia':
            return self.energia
        if atributo == 'Agilidad':
            return self.agilidad

    @property
    def resistencia(self):
        valor = 0
        for carta in self.recursos:
            if carta.subtipo == 'Resistencia' and carta.activa:
                valor += carta.valor
        return valor

    @property
    def energia(self):
        valor = 0
        for carta in self.recursos:
            if carta.subtipo == 'Energia' and carta.activa:
                valor += carta.valor
        return valor

    @property
    def agilidad(self):
        valor = 0
        for carta in self.recursos:
            if carta.subtipo == 'Agilidad' and carta.activa:
                valor += carta.valor
        return valor

    @property
    def pesoResistencia(self):
        valor = 0
        for carta in self.recursos:
            if carta.subtipo == 'Resistencia':
                valor += carta.peso
        return valor

    @property
    def pesoEnergia(self):
        valor = 0
        for carta in self.recursos:
            if carta.subtipo == 'Energia':
                valor += carta.peso
        return valor

    @property
    def pesoAgilidad(self):
        valor = 0
        for carta in self.recursos:
            if carta.subtipo == 'Agilidad':
                valor += carta.peso
        return valor

    @property
    def imagen(self):
        if self._imagen:
            return self._imagen
        else:
            self._imagen = transform.scale(
                image.load(path.join(CA, self.arte)),
                (125, 182))
            return self._imagen

    def __getstate__(self):
        self._imagen = None
        return self.__dict__

    def __str__(self):
        return '{}(R:{}, E:{}, A:{})'.format(self.nombre, self.resistencia, self.energia, self.agilidad)

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

    def __nonzero__(self):
        return self.activo


class Pos(object):
    """Objeto que representa una posicion en X y Y"""

    def __init__(self, x=0, y=0):
        self.x = x
        self.y = y

    _x = 0

    @property
    def x(self):
        return self._x

    @x.setter
    def x(self, valor):
        self._x = valor

    _y = 0
    @property
    def y(self):
        return self._y

    @y.setter
    def y(self, valor):
        self._y = valor

    def __eq__(self, objeto):
        try:
            if objeto.x == self.x and objeto.y == self.y:
                return True
            else:
                return False
        except AttributeError:
            return NotImplemented

    def __nonzero__(self):
        return (self.x is not None) and (self.y is not None)

    def __hash__(self):
        return int(str(id(self.x))+str(id(self.y)))

    def __str__(self):
        return "({},{})".format(self.x,self.y)

    def __repr__(self):
        return  "(x={}, y={})".format(self.x, self.y)

    def __add__(self, valor):
        """Pos cuyo X y Y son la suma de las Pos"""
        return Pos(x=(self.x+valor.x), y=(self.y+valor.y))

    def __radd__(self, valor):
        return self.__add__(valor)

    def __iadd__(self, valor):
        """Aumenta los X y Y pór los del valor"""
        self.x += valor.x
        self.y += valor.y
        return self

    def __sub__(self, valor):
        """Pos cuyo X y Y son la resta de las Pos"""
        return Pos(x=(self.x-valor.x), y=(self.y-valor.y))

    def __rsub__(self, valor):
        return self.__sub__(valor)

    def __isub__(self, valor):
        """Disminuye los X y Y por los del valor"""
        self.x -= valor.x
        self.y -= valor.y
        return self

    def __int__(self):
        return abs(self.x) + abs(self.y)

    def __float__(self):
        return (self.x**2 + self.y**2)**(1/2)



class listaPersonajes(object):
    """Contenedor que mantiene el orden de jugada"""

    nivel = 0

    def __init__(self, personajes):
        self.personajes = personajes

    def __iter__(self):
        """Reorganiza a los personajes por nivel de energia"""
        self.nivel, periodos = self._calcular_orden()
        return self

    def next(self):
        if self.nivel < 0:
            raise StopIteration
        else:
            nivel, periodos = self._calcular_orden()
            personajes = periodos[self.nivel]
            self.nivel -= 1
            return personajes

    def _calcular_orden(self):
        personajes = [
            (personaje.energia, personaje)
            for personaje in self.personajes
            if personaje.activo]
        try:
            maximo = max([personaje[0] for personaje in personajes])
        except ValueError:
            maximo = 0
        periodos = {}
        for periodo in range(maximo, -1, -1):
            periodos[periodo] = [
                personaje[1]
                for personaje in personajes
                if personaje[0] >= periodo]
        return maximo, periodos

    @property
    def personajesActivos(self):
        maximo, periodos = self._calcular_orden()
        try:
            return periodos[self.nivel + 1]
        except KeyError:
            return []
