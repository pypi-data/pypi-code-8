#!/usr/bin/env python
# -*- coding: utf-8 -*-

from logging import getLogger
REG = getLogger('Cartas')

from StringIO import StringIO
from glob import glob
from os import path
from copy import copy

from lxml.etree import parse, DTD, tostring, XMLParser
from pygame import image, Surface, transform

from Cambios.generador import ProducirImagen


CA = path.join(path.abspath(path.dirname(__file__)), 'Arte')
CP = path.join(path.abspath(path.dirname(__file__)), 'PreGeneradas')

ARCHIVO_DTD = StringIO(
"""<!ELEMENT carta (nombre,  clases, nivel?, peso?, valor?, atributos?, habilidad?, imagen, metadatos)>
<!ATTLIST carta tipo (Personaje|Habilidad|Recurso) #REQUIRED subtipo CDATA ''>

<!ELEMENT nombre (#PCDATA)>

<!ELEMENT clases (clase*)>
<!ELEMENT clase (#PCDATA)>

<!ELEMENT nivel (#PCDATA)>

<!ELEMENT peso (#PCDATA)>
<!ELEMENT valor (#PCDATA)>

<!ELEMENT atributos (salud, consentracion, agilidad)>
<!ELEMENT salud (#PCDATA)>
<!ELEMENT consentracion (#PCDATA)>
<!ELEMENT agilidad (#PCDATA)>

<!ELEMENT habilidad (titulo, activacion, costo, efecto+, extra)>
<!ELEMENT titulo (#PCDATA)>
<!ELEMENT activacion (#PCDATA)>
<!ELEMENT costo (token*)>
<!ELEMENT efecto (#PCDATA|token)*>
<!ELEMENT extra (token*)>
<!ELEMENT token EMPTY>
<!ATTLIST token tipo CDATA #REQUIRED valor CDATA '1'>

<!ELEMENT imagen (titulo, alternativo, artista+)>
<!ATTLIST imagen archivo CDATA 'Fondo.png'>
<!ELEMENT titulo (#PCDATA)>
<!ELEMENT alternativo (#PCDATA)>
<!ELEMENT artista (#PCDATA)>

<!ELEMENT metadatos (temporada, expancion, serial, vercion)>
<!ATTLIST metadatos licencia CDATA #FIXED "®Tierras extrañas: Escaramusas, por Wolfang Torres, Todos los derechos reservados">
<!ELEMENT temporada (#PCDATA)>
<!ATTLIST temporada numero CDATA '1'>
<!ELEMENT expancion (#PCDATA)>
<!ATTLIST expancion numero CDATA '1'>
<!ELEMENT serial (#PCDATA)>
<!ELEMENT vercion (#PCDATA)>"""
)


class Metadatos(object):
    """Componente de Carta que representa la informacion de identificacion"""

    licencia = "®Tierras extrañas: Escaramusas, por Wolfang Torres, Todos los derechos reservados"

    def __init__(self, temporada=0, expancion=0, serial=0, vercion=0, nombreTemporada='', nombreExpancion=''):
        self.temporada = int(temporada)
        self.expancion = int(expancion)
        self.serial = serial
        self.vercion = vercion

        self.nombreTemporada = nombreTemporada
        self.nombreExpancion = nombreExpancion

    def __hash__(self):
        return int('1{0:02d}{1:02d}{2:02d}{3:02d}'.format(
            int(self.temporada) if self.temporada else 0,
            int(self.expancion) if self.expancion else 0,
            int(self.serial) if self.serial else 0,
            int(self.vercion) if self.vercion else 0)
            )


class Imagen(object):
    """Objeto que representa la imagen de una Carta y sus Metadatos"""

    _imagen = None

    def __init__(self, archivo='', titulo='', alternativo='', artista=''):
        self.archivo = archivo if archivo else 'Fondo.png'
        self.titulo = titulo
        self.alternativo = alternativo
        self.artista = artista


class Efecto(object):
    """Objeto que contiene la informacion de una habilidad y su efecto en el juego"""

    def __init__(self, titulo='', activacion='', costo=(), efecto=(), extra=()):
        self.titulo = titulo
        self.activacion = activacion
        self.costo = costo
        self.efecto = efecto
        self.extra = extra

    def __str__(self):
        l = []
        for efecto in self.efecto:
            e = ''
            for f in efecto:
                e += str(f)
            l.append(e)
        return '{}: '.format(self.titulo) + ' - '.join(l)


class Token(object):
    """Objeto que representa una cantidad de un tipo de objetos"""

    def __init__(self, tipo='', valor=1):
        self.tipo = tipo
        self.valor = valor

    def __str__(self):
        return '{} {}'.format(self.valor, self.tipo)


class Carta(object):
    """Clase base para Cartas"""

    _png = None
    _activa = True

    def __init__(self, nombre='', tipo='', subtipo='', clases=(),
                 metadatos=Metadatos(), imagen=Imagen(), efecto=None,
                 archivo=None):
        self.nombre = nombre
        self.tipo = tipo
        self.subtipo = subtipo
        self.clases = clases

        self.efecto = efecto

        self.imagen = imagen
        self.metadatos = metadatos

        self.archivo = archivo

    @property
    def activa(self):
        return bool(self._activa)

    @activa.setter
    def activa(self, valor):
        self._activa = bool(valor)

    def __nonzero__(self):
        return self.activa

    def __hash__(self):
        return hash(self.metadatos)

    def __eq__(self, carta):
        if type(carta) is type(self):
            if hash(carta) == hash(self):
                return True
        else:
            return NotImplemented

    def __str__(self):
        v = (None, None, None)
        if self.tipo == 'Recurso':
            v = (unicode(self.nombre), self.tipo, self.subtipo)
        elif self.tipo == 'Habilidad':
            v = (unicode(self.nombre), self.tipo, unicode(self.efecto.titulo))
        elif self.tipo == 'Personaje':
            v = (unicode(self.nombre), self.tipo, 'N{}'.format(self.nivel))
        t = u'{}({}-{})'.format(*v)
        return unicode(t).encode('utf-8')

    def __getstate__(self):
        self._png = None
        return self.__dict__

    @property
    def png(self):
        if self._png:
            return self._png
        elif path.join(CP,'{}.png'.format(hash(self))) in glob(path.join(CP, '*.png')):
            archivo = path.join(CP, '{}.png'.format(hash(self)))
            self._png = transform.scale(image.load(archivo), (103, 150))
            return self._png
        elif self.archivo:
            xml = parse(self.archivo, XMLParser(dtd_validation=False)).getroot()
            archivo = ProducirImagen(xml, hash(self))
            self._png = transform.scale(image.load(archivo), (103, 150))
            return self._png
        else:
            return None


class Recurso(Carta):
    """Tipo de Carta, los Recursos son los atributos de los Personajes"""

    tipo = 'Recurso'

    def __init__(self, nombre='', subtipo='', clases=(),
                 peso=1, valor=1, efecto=None,
                 metadatos=Metadatos(), imagen=Imagen(),
                 archivo=None):

        self.nombre = nombre
        self.subtipo = subtipo
        self.clases = clases

        self.peso = int(peso)
        self.valor = int(valor)

        self.efecto = efecto

        self.imagen = imagen
        self.metadatos = metadatos

        self.archivo = archivo


class Habilidad(Carta):
    """Tipo de Carta, Las Habilidades son las capasidades de los Personaje"""

    tipo = 'Habilidad'

    def __init__(self, nombre='', subtipo='', clases=(), efecto=None,
                 metadatos=Metadatos(), imagen=Imagen(),
                 archivo=None):

        self.nombre = nombre
        self.subtipo = subtipo
        self.clases = clases

        self.efecto = efecto

        self.imagen = imagen
        self.metadatos = metadatos

        self.archivo = archivo


class Personaje(Carta):
    """Tipo de Carta, Los Personajes representan las unidades bajo tu control"""

    tipo = 'Personaje'

    def __init__(self, nombre='', clases=(), nivel=0,
                 salud=0, consentracion=0, movilidad=0, efecto=None,
                 metadatos=Metadatos(), imagen=Imagen(),
                 archivo=None):

        self.nombre = nombre
        self.clases = clases

        self.nivel = int(nivel)

        self.salud = int(salud)
        self.consentracion = int(consentracion)
        self.movilidad = int(movilidad)

        self.efecto = efecto

        self.imagen = imagen
        self.metadatos = metadatos

        self.archivo = archivo


class MasoCartas(list):
    """Contenedor que representa un Maso de Cartas"""

    def __init__(self, tamano=10):
        list.__init__(self)
        self.tamano = tamano
        self.extend([None for i in range(tamano)])

    def tomar(self, cantidad=1):
        self.extend([None for i in range(cantidad)])
        cartas = [self.pop(0) for i in range(cantidad)]
        return cartas

    def agregar(self, cartas):
        for carta in cartas:
            carta.activa = True
        for carta in range(self.tamano-1,-1,-1):
            if self[carta] is None:
                del self[carta]
        if len(cartas) <= (self.tamano - len(self)):
            self.extend(cartas)
            self.extend([None for i in range(self.tamano-len(self))])
        else:
            raise Exception('El maso esta lleno')

    def __len__(self):
        n = 0
        for i in self:
            if not i is None:
                n += 1
        return n


def CrearCartaXML(archivo, dtd):
    """Crea un objeto Carta desde un archivo XML"""
    xml = parse(archivo, XMLParser(dtd_validation=False)).getroot()
    if not dtd.validate(xml):
        raise Exception(dtd.error_log.filter_from_errors()[0])

    efecto = None
    for nodo in xml:
        if nodo.tag == 'imagen':
            imagen = CrearImagenXML(nodo)
        if nodo.tag == 'metadatos':
            metadatos = CrearMetadatosXML(nodo)
        if nodo.tag == 'habilidad':
            efecto = CrearEfectoXML(nodo)

    if xml.get('tipo') == 'Recurso':
        carta = Recurso(
            archivo=archivo,
            nombre=xml[0].text,
            subtipo=xml.get('subtipo'),
            clases=[clase.text for clase in xml[1]],
            peso=xml[2].text,
            valor=xml[3].text,
            efecto=efecto,
            imagen=imagen,
            metadatos=metadatos,
            )

    if xml.get('tipo') == 'Habilidad':
        carta = Habilidad(
            archivo=archivo,
            nombre=xml[0].text,
            subtipo=xml.get('subtipo'),
            clases=[clase.text for clase in xml[1]],
            efecto=efecto,
            imagen=imagen,
            metadatos=metadatos,
            )

    if xml.get('tipo') == 'Personaje':
        carta = Personaje(
            archivo=archivo,
            nombre=xml[0].text,
            clases=[clase.text for clase in xml[1]],
            nivel=xml[2].text,
            salud=xml[3][0].text,
            consentracion=xml[3][1].text,
            movilidad=xml[3][2].text,
            efecto=efecto,
            imagen=imagen,
            metadatos=metadatos,
            )

    return carta


def CrearImagenXML(nodo):
    """Crea un objeto Imagen desde un nodo XML"""
    return Imagen(archivo=nodo.get('archivo'), titulo=nodo[0].text,
                  alternativo=nodo[1].text, artista=nodo[2].text)


def CrearMetadatosXML(nodo):
    """Crea un objeto Metadatos desde un nodo XML"""
    return Metadatos(temporada=nodo[0].get('numero'),
                     expancion=nodo[1].get('numero'),
                     serial=nodo[2].text,
                     vercion=nodo[3].text,
                     nombreTemporada=nodo[0].text,
                     nombreExpancion=nodo[1].text)


def CrearEfectoXML(nodo):
    """Crea un objeto Efecto desde un nodo XML"""
    titulo = nodo[0].text.encode('utf-8')
    activacion = nodo[1].text.encode('utf-8')
    costo = []
    for a in (a for a in nodo if a.tag == 'costo'):
        costo = [Token(t.get('tipo'), t.get('valor')) for t in a]

    extra = ()
    for a in (a for a in nodo if a.tag == 'extra'):
        extra = [Token(t.get('tipo'), t.get('valor')) for t in a]

    efecto = []
    for a in (a for a in nodo if a.tag == 'efecto'):
        e = []
        e.append(a.text)
        for t in a:
            e.append(Token(t.get('tipo'), t.get('valor')))
            e.append(t.tail)
        efecto.append(e)
    return Efecto(titulo=titulo, activacion=activacion,
                  costo=costo, efecto=efecto, extra=extra)


def BuscarCarta(codigo):
    for carta in CARTAS:
        if hash(carta) == codigo:
            return copy(carta)
    raise Exception('Carta no encontrada')

archivos = glob(path.join(path.abspath(path.dirname(__file__)), 'Cartas', '*.xml'))
dtd = DTD(ARCHIVO_DTD)
CARTAS = [CrearCartaXML(carta, dtd) for carta in archivos]
REG.debug('Base local de cartas generada')
