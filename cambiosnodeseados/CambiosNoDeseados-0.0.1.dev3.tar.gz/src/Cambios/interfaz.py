#!/usr/bin/env python
# -*- coding: utf-8 -*-

from logging import getLogger
REG = getLogger('Interfaz')

import sys
from os import path

import pygame
from pygame.locals import *
from pygame import event, font, Color, Surface, Rect, image, transform

from Cambios.juego import Mapa, Personaje, Pos
from Cambios.reglas import Reglas, Accion, Movimiento, Esperar, Acoplar, Habilidad
from Cambios.reglas import CAMPOSELECCIONADO, COMANDOSELECCIONADO, CARTASELECCIONADA


pygame.init()

VENTANA_ANCHO, VENTANA_ALTO = 800, 600

CR = path.join(path.abspath(path.dirname(__file__)), 'Recursos')
CA = path.join(path.abspath(path.dirname(__file__)), 'Arte')
CI = path.join(path.abspath(path.dirname(__file__)), 'Iconos')
CL = path.join(path.abspath(path.dirname(__file__)), 'Letras')
RECURSOS = {
    'fondo' : transform.scale(
        image.load(path.join(CR, 'flippybackground.png')),
        (VENTANA_ANCHO, VENTANA_ALTO)),
    'piso' : image.load(path.join(CR, 'Plain_Block.png')),
    'grama' : image.load(path.join(CR, 'Grass_Block.png')),
    'piedra' : image.load(path.join(CR, 'Rock.png')),
    'arbol' : image.load(path.join(CR, 'Tree_Ugly.png')),
    'esquina' : image.load(path.join(CR, 'Wall_Block_Tall.png')),
    'pared' : image.load(path.join(CR, 'Wood_Block_Tall.png')),
    'selectorAmigo' :  image.load(path.join(CR, 'Selector.png')),
    'selectorEnemigo' :  image.load(path.join(CR, 'RedSelector.png')),
        }
PERSONAJES = {
    'personaje1' : image.load(path.join(CR, 'boy.png')),
    'personaje2' : image.load(path.join(CR, 'catgirl.png')),
    'personaje3' : image.load(path.join(CR, 'horngirl.png')),
    'Alma Roja' : image.load(path.join(CR, 'AlmaRoja.png')),
    'Alma Azul' : image.load(path.join(CR, 'AlmaAzul.png')),
    'Alma Amarilla' : image.load(path.join(CR, 'AlmaAmarilla.png')),
    'Alma Blanca' : image.load(path.join(CR, 'AlmaBlanca.png')),
        }
TRANSPARENTE = Color(0, 0, 0, 0)
BLANCO = Color(255, 255, 255, 255)
NEGRO = Color(0, 0, 0, 255)
ROJO = Color(255, 0, 0, 255)
VERDE = Color(0, 255, 0, 255)
AZUL = Color(0, 0, 255)
AMARILLO = Color(255, 255,   0)
LETRA_GRANDE = font.Font(path.join(CL, 'LinBiolinum_R.otf'), 32)
LETRA_MEDIANA = font.Font(path.join(CL, 'LinBiolinum_R.otf'), 24)
LETRA_PEQUENA = font.Font(path.join(CL, 'LinBiolinum_R.otf'), 16)


class Interfaz(object):
    """Clase Principal"""

    TITULO = 'Cambios No deseados'
    FPS = 30

    CAMARA = [VENTANA_ANCHO/2, VENTANA_ALTO/2]
    CAMARA_VELOCIDAD = [0, 0]
    VELOCIDAD_DE_CAMARA = 40
    CAMARA_LIMITES = [300, 300]

    AREAS = [Rect((0, 0), (VENTANA_ANCHO, VENTANA_ALTO))]
    AREAS_VIEJAS = []

    MOUSE = (0, 0)

    personajeSeleccionado = None

    def __init__(self):
        self.Reloj = pygame.time.Clock()
        self.Pantalla = pygame.display.set_mode(
            (VENTANA_ANCHO, VENTANA_ALTO),
            HWSURFACE|DOUBLEBUF|RESIZABLE)
        pygame.display.set_caption(self.TITULO)

        self.Campo = Campo()
        self.MedidorTurno = MedidorTurno()
        self.ZonaCartas = ZonaCartas()
        self.MostradorPersonaje = MostradorPersonaje()

    def bucleGUI(self):
        self.bucleEventos()

        self.Pantalla.blit(RECURSOS['fondo'], (0, 0))
        self.ActualizarCamara()
        if self.juego and self.jugador:
            self.CrearMapa()
            self.DibujarMostrador()
            self.DibujarHUD()
            self.DibujarZonaCartas()

        pygame.display.update(self.AREAS + self.AREAS_VIEJAS)
        self.AREAS_VIEJAS = self.AREAS
        self.AREAS = []

    def bucleEventos(self):
        for evento in event.get():
            # envetos del sistema
            if evento.type == QUIT:
                pygame.quit()
                sys.exit()
            elif evento.type == KEYDOWN:
                if evento.key in (K_UP, K_w):
                    self.CAMARA_VELOCIDAD[1] += 1
                if evento.key in (K_DOWN, K_s):
                    self.CAMARA_VELOCIDAD[1] -= 1
                if evento.key in (K_RIGHT, K_d):
                    self.CAMARA_VELOCIDAD[0] -= 1
                if evento.key in (K_LEFT, K_a):
                    self.CAMARA_VELOCIDAD[0] += 1
            elif evento.type == KEYUP:
                if evento.key in (K_UP, K_w):
                    self.CAMARA_VELOCIDAD[1] = 0
                if evento.key in (K_DOWN, K_s):
                    self.CAMARA_VELOCIDAD[1] = 0
                if evento.key in (K_RIGHT, K_d):
                    self.CAMARA_VELOCIDAD[0] = 0
                if evento.key in (K_LEFT, K_a):
                    self.CAMARA_VELOCIDAD[0] = 0
            elif evento.type == MOUSEMOTION:
                self.MOUSE = evento.pos
            elif evento.type == MOUSEBUTTONDOWN:
                self.MOUSE = evento.pos
                self.click(evento.button)
            elif evento.type == VIDEORESIZE:
                global VENTANA_ALTO, VENTANA_ANCHO
                VENTANA_ALTO = evento.h if evento.h > 600 else 600
                VENTANA_ANCHO = evento.w if evento.w > 800 else 800
                RECURSOS['fondo'] = transform.scale(
                    image.load(path.join(CR, 'flippybackground.png')),
                    (VENTANA_ANCHO, VENTANA_ALTO))
                self.Pantalla = pygame.display.set_mode(
                    (VENTANA_ANCHO, VENTANA_ALTO),
                    HWSURFACE|DOUBLEBUF|RESIZABLE)
                self.AREAS.append(self.Pantalla.get_bounding_rect())
            # Eventos del juego
            elif evento.type == CAMPOSELECCIONADO:
                if self.ACCION_ACTIVA:
                    self.ACCION_ACTIVA.agregarVariable(evento)
                    continue
                self.seleccionarPersonaje(evento.objetivo)
            elif evento.type == CARTASELECCIONADA:
                if self.ACCION_ACTIVA:
                    self.ACCION_ACTIVA.agregarVariable(evento)
                    continue
            elif evento.type == COMANDOSELECCIONADO:
                if evento.comando == 'cancelar' or evento.comando is None:
                    self.ACCION_ACTIVA = None
                    self.personajeSeleccionado = None
                elif evento.comando == 'esperar':
                    self.ACCION_ACTIVA = Esperar(evento.personaje)
                elif evento.comando == 'mover':
                    self.ACCION_ACTIVA = Movimiento(evento.personaje)
                elif evento.comando == 'acoplar':
                    self.ACCION_ACTIVA = Acoplar(evento.personaje)
                else:
                    self.ACCION_ACTIVA = Habilidad(self.jugador, evento.personaje, evento.comando)

    def click(self, boton):
        '''Maneja eventos MOUSEBUTTONDOWN del sistema y crea eventos del juego'''
        if boton == 1:
            if self.personajeSeleccionado and self.MostradorPersonaje.Area.collidepoint(*self.MOUSE):
                e = event.Event(
                    COMANDOSELECCIONADO,
                    comando=self.seleccionarAccion(self.MOUSE),
                    personaje=self.personajeSeleccionado,)
                event.post(e)
            elif self.jugador and self.ZonaCartas.Area.collidepoint(*self.MOUSE):
                c, p = self.seleccionarCarta(self.MOUSE)
                e = event.Event(CARTASELECCIONADA, carta=c, pos=p)
                event.post(e)
            elif self.juego and self.Campo.Area.collidepoint(*self.MOUSE):
                p = self.seleccionarPos(self.MOUSE)
                e = event.Event(CAMPOSELECCIONADO, objetivo=p)
                event.post(e)

    def ActualizarCamara(self):
        x, y = self.CAMARA
        x += self.CAMARA_VELOCIDAD[0] * self.VELOCIDAD_DE_CAMARA
        y += self.CAMARA_VELOCIDAD[1] * self.VELOCIDAD_DE_CAMARA
        if abs(x-(VENTANA_ANCHO/2)) <= self.CAMARA_LIMITES[0]:
           self.CAMARA[0] = x
        if abs(y-(VENTANA_ALTO/2)) <= self.CAMARA_LIMITES[1]:
           self.CAMARA[1] = y

    def seleccionarPos(self, mouse):
        '''Regresa las cordenadas de un cuadro del mapa apartir del mouse'''
        x = mouse[0] - self.Campo.Area.left
        y = mouse[1] - self.Campo.Area.top
        return self.Campo.buscarCuadro(x, y)

    def seleccionarPersonaje(self, pos):
        '''seleciona un personaje para mostrar en el mostrador'''
        self.personajeSeleccionado = None
        codigo = self.juego.mapa[pos] if bool(pos) else None
        self.personajeSeleccionado = codigo

    def seleccionarCarta(self, mouse):
        '''seleciona una carta para mostrar'''
        self.cartaSeleccionada = None
        x = mouse[0] - self.ZonaCartas.Area.left
        y = mouse[1] - self.ZonaCartas.Area.top
        carta, pos = self.ZonaCartas.buscarCarta(x, y)
        self.cartaSeleccionada = carta
        return carta, pos

    def seleccionarAccion(self, mouse):
        if not self.juego.buscarPersonaje(self.personajeSeleccionado) in self.juego.personajesActivos:
            return None
        x = mouse[0] - self.MostradorPersonaje.Area.left
        y = mouse[1] - self.MostradorPersonaje.Area.top
        comando = self.MostradorPersonaje.buscarComando(x, y)
        return comando

    def funMover(self):
        # definido en main
        pass

    def DibujarMostrador(self):
        if self.personajeSeleccionado:
            self.MostradorPersonaje.actualizar(
                self.reglas,
                self.jugador,
                self.personajeSeleccionado,
                )
            self.MostradorPersonaje.Area.topleft = (10, 10)
            self.AREAS.append(self.MostradorPersonaje.Area)
            self.Pantalla.blit(
                self.MostradorPersonaje.Superficie,
                self.MostradorPersonaje.Area)

    def CrearMapa(self):
        self.Campo.actualizar(self.juego, self.jugador, self.ACCION_ACTIVA)
        self.Campo.Area.center = self.CAMARA
        self.AREAS.append(self.Campo.Area)
        self.Pantalla.blit(self.Campo.Superficie, self.Campo.Area)

    def DibujarHUD(self):
        self.MedidorTurno.actualizar(self.juego, self.jugador, self.reglas.personajesOcupados)
        self.MedidorTurno.Area.topright = (VENTANA_ANCHO-10, 10)
        self.AREAS.append(self.MedidorTurno.Area)
        self.Pantalla.blit(self.MedidorTurno.Superficie, self.MedidorTurno.Area)

    def DibujarZonaCartas(self):
        self.ZonaCartas.actualizar(self.jugador)
        self.ZonaCartas.Area.bottomleft = (10, VENTANA_ALTO-10)
        self.AREAS.append(self.ZonaCartas.Area)
        self.Pantalla.blit(self.ZonaCartas.Superficie, self.ZonaCartas.Area)


class MedidorTurno(object):
    """Objeto que muestra el orden de los turnos"""

    def actualizar(self, juego, jugador, personajesOcupados):
        self.juego = juego
        self.jugador = jugador
        self.personajesOcupados = personajesOcupados
        self.Area = Rect((0,0), (150, 400))
        self.Superficie = Surface((self.Area.width, self.Area.height)).convert_alpha()
        self.Superficie.fill(TRANSPARENTE)

        turno = LETRA_GRANDE.render('Turno {}'.format(juego.numeroTurno), True, NEGRO)
        a = turno.get_rect()
        a.topleft = (0, 0)
        self.Superficie.blit(turno, a)
        pygame.draw.line(self.Superficie, NEGRO, a.bottomleft, a.bottomright, 5)

        periodo = LETRA_MEDIANA.render('Periodo {}'.format(juego.numeroPeriodo), True, NEGRO)
        b = periodo.get_rect()
        b.topleft = a.bottomleft
        b.top += 10
        self.Superficie.blit(periodo, b)

        personajes = self.juego.personajesActivos
        for p in range(len(personajes)):
            if hash(personajes[p]) in self.jugador.personajes:
                color = AMARILLO
            else:
                color = ROJO
            if hash(personajes[p]) in self.personajesOcupados:
                color = NEGRO

            personaje = LETRA_PEQUENA.render(personajes[p].nombre, True, color)
            a = personaje.get_rect()
            a.topleft = (20, (20*p) + b.bottom)
            self.Superficie.blit(personaje, a)


class ZonaCartas(object):
    """Objeto que representa el lugar donde van el mazo y la mano de cartas"""

    ALTURA = 150
    ANCHO_CARTA = 103
    CARTAS_MASO = 10
    ALTO_FONDO = ALTURA-(5*(CARTAS_MASO-1))
    ANCHO_FONDO = 59*ALTO_FONDO/86
    FONDO = transform.scale(
        image.load(path.join(CA, 'Fondo.png')),
        (ANCHO_FONDO, ALTO_FONDO))

    def actualizar(self, jugador):
        self.jugador = jugador
        self.Area = Rect((0, 0), (VENTANA_ANCHO-20, self.ALTURA))
        self.Superficie = Surface((self.Area.width, self.Area.height)).convert_alpha()
        self.Superficie.fill(TRANSPARENTE)

        self.maso = Rect((0,0), ((self.Area.width*0.2)-5, self.Area.height))
        Maso = Surface((self.maso.width, self.maso.height)).convert_alpha()
        Maso.fill(TRANSPARENTE)
        for l in range(self.CARTAS_MASO*len(jugador.maso)//jugador.maso.tamano):
            x = 5 * l
            y = 5 * (self.CARTAS_MASO - (l + 1))
            Maso.blit(self.FONDO, (x, y))

        self.mano = Rect(
            ((self.Area.width*0.2)+5, 0),
            (self.Area.width*0.8, self.Area.height))
        Mano = Surface((self.mano.width, self.mano.height)).convert_alpha()
        Mano.fill(TRANSPARENTE)
        for c in range(len(self.jugador.mano)):
            x = c * ((self.mano.width-self.ANCHO_CARTA)/len(self.jugador.mano))
            a = Rect((x, 0), (self.ANCHO_CARTA, self.ALTURA))
            Mano.blit(self.jugador.mano[c].png, a)

        self.Superficie.blit(Maso, self.maso)
        self.Superficie.blit(Mano, self.mano)

    def buscarCarta(self, X, Y):
        if not self.mano.collidepoint(X, Y):
            return None, None
        X -= self.mano.left
        Y -= self.mano.top
        for c in range(len(self.jugador.mano)-1, -1, -1):
            x = c * ((self.mano.width-self.ANCHO_CARTA)/len(self.jugador.mano))
            a = Rect((x, 0), (self.ANCHO_CARTA, self.ALTURA))
            if a.collidepoint(X, Y):
                return self.jugador.mano[c], c
        return None, None


class MostradorPersonaje(object):
    """Objeto que muestra la informacion del personaje"""

    R = transform.scale(image.load(path.join(CI, 'CResistencia.png')), (50, 50))
    E = transform.scale(image.load(path.join(CI, 'CEnergia.png')), (50, 50))
    A = transform.scale(image.load(path.join(CI, 'CAgilidad.png')), (50, 50))

    def actualizar(self, reglas, jugador, personaje):
        self.reglas = reglas
        self.jugador = jugador
        self.personaje = self.reglas.juego.buscarPersonaje(personaje)
        self.Area = Rect((10,10), (200, VENTANA_ALTO-150-30))
        self.Superficie = Surface((self.Area.width, self.Area.height)).convert_alpha()
        self.Superficie.fill(TRANSPARENTE)

        self.crearVista()
        if ((hash(self.personaje) in self.jugador.personajes) and
            (self.personaje in self.reglas.juego.personajesActivos) and
            (hash(self.personaje) not in self.reglas.personajesOcupados)):
               self.crearMenu()

    def crearVista(self):
        imagen = Rect((0,0), (125, 182))
        self.Superficie.blit(self.personaje.imagen, imagen)

        for i in range(3):
            a = (self.R, self.E, self.A)[i]
            atrib = Rect((135, i*182/3), (65, 182/3))
            self.Superficie.blit(a, atrib)
            if a == self.R:
                v = LETRA_GRANDE.render(str(self.personaje.resistencia), True, BLANCO)
            if a == self.E:
                v = LETRA_GRANDE.render(str(self.personaje.energia), True, BLANCO)
            if a == self.A:
                v = LETRA_GRANDE.render(str(self.personaje.agilidad), True, BLANCO)
            p = v.get_rect()
            p.center = atrib.center
            p.left -= 6
            p.top -= 4
            self.Superficie.blit(v, p)

        n = Rect((0, 187), (200, 20))
        Nombre = LETRA_MEDIANA.render(str(self.personaje.nombre), True, NEGRO)
        nombre = Nombre.get_rect()
        nombre.center = n.center
        self.Superficie.blit(Nombre, nombre)

    def crearMenu(self):
        self.menu = Rect((0,212), (200, VENTANA_ALTO-150-30-192))
        Menu = Surface((self.menu.width, self.menu.height)).convert_alpha()
        Menu.fill(TRANSPARENTE)
        self.MapeoComandos = {}

        x = ((0,0), (200, 20))
        e = Rect(*x)
        f = Surface((e.width, e.height)).convert_alpha()
        f.fill(NEGRO)
        Menu.blit(f, e)
        Esperar = LETRA_PEQUENA.render('Esperar', True, BLANCO)
        esperar = Esperar.get_rect()
        esperar.center = e.center
        Menu.blit(Esperar, esperar)
        self.MapeoComandos[x] = 'esperar'

        x = ((0,25), (200, 20))
        m = Rect(*x)
        f = Surface((m.width, m.height)).convert_alpha()
        f.fill(NEGRO)
        Menu.blit(f, m)
        Mover = LETRA_PEQUENA.render('Mover', True, BLANCO)
        mover = Mover.get_rect()
        mover.center = m.center
        Menu.blit(Mover, mover)
        self.MapeoComandos[x] = 'mover'

        x = ((0,50), (200, 20))
        a = Rect(*x)
        f = Surface((a.width, a.height)).convert_alpha()
        f.fill(NEGRO)
        Menu.blit(f, a)
        Acoplar = LETRA_PEQUENA.render('Acoplar Carta', True, BLANCO)
        acoplar = Acoplar.get_rect()
        acoplar.center = a.center
        Menu.blit(Acoplar, acoplar)
        self.MapeoComandos[x] = 'acoplar'

        x = ((0,75), (200, 20))
        a = Rect(*x)
        f = Surface((a.width, a.height)).convert_alpha()
        f.fill(NEGRO)
        Menu.blit(f, a)
        Cancelar = LETRA_PEQUENA.render('Cancelar', True, BLANCO)
        cancelar = Cancelar.get_rect()
        cancelar.center = a.center
        Menu.blit(Cancelar, cancelar)
        self.MapeoComandos[x] = 'cancelar'

        n = 0
        for carta in self.personaje.habilidades:
            n += 1
            x = ((0, 75+(25*n)), (200, 20))
            a = Rect(*x)
            f = Surface((a.width, a.height)).convert_alpha()
            f.fill(BLANCO)
            Menu.blit(f, a)
            letra = LETRA_PEQUENA.render(carta.efecto.titulo.decode('utf-8'), True, NEGRO)
            c = letra.get_rect()
            c.center = a.center
            Menu.blit(letra, c)
            self.MapeoComandos[x] = carta.efecto.titulo

        self.Superficie.blit(Menu, self.menu)

    def buscarComando(self, x, y):
        if not self.menu.collidepoint(x, y):
            return None
        x = x - self.menu.left
        y = y - self.menu.top
        for area, comando in self.MapeoComandos.items():
            if Rect(*area).collidepoint(x, y):
                return comando


class Campo(object):
    """Objeto que representa el campo de juego"""

    CUADRO_ALTO = 85
    CUADRO_ANCHO = 50
    PISO_TOPE = 24
    PISO_CUERPO = 44
    PISO_FONDO = 17

    def actualizar(self, juego, jugador, accionActiva):
        self.juego = juego
        self.jugador = jugador
        self.accionActiva = accionActiva
        self.Area = Rect((0,0),
            (juego.mapa.totX*self.CUADRO_ANCHO,
            (self.PISO_TOPE + (self.PISO_CUERPO*juego.mapa.totY) + self.PISO_FONDO)
            ))
        self.Superficie = Surface((self.Area.width, self.Area.height)).convert_alpha()
        self.Superficie.fill(TRANSPARENTE)

        for pos, (fondo, objeto) in juego.mapa.lista():
            c = Rect(pos.x*self.CUADRO_ANCHO,
                (pos.y*self.PISO_CUERPO),
                self.CUADRO_ANCHO, self.CUADRO_ALTO)
            # Fondo
            if fondo in RECURSOS:
                self.Superficie.blit(RECURSOS[fondo], c)
            # Acciones
            if self.accionActiva and self.accionActiva.tipo == 'movimiento':
                p = juego.mapa.buscar(accionActiva.personaje)
                if pos in (Pos(p.x+1,p.y),Pos(p.x-1,p.y),Pos(p.x,p.y+1),Pos(p.x,p.y-1)):
                    if fondo in ('piso', 'grama'):
                        self.Superficie.blit(RECURSOS['selectorAmigo'], c)
            # Frente
            personaje = self.juego.buscarPersonaje(objeto)
            if not personaje is None:
                if hash(personaje) in self.jugador.personajes:
                    self.Superficie.blit(RECURSOS['selectorAmigo'], c)
                else:
                    self.Superficie.blit(RECURSOS['selectorEnemigo'], c)
                if personaje.nombre in PERSONAJES:
                    self.Superficie.blit(PERSONAJES[personaje.nombre], c)
                else:
                    self.Superficie.blit(PERSONAJES['personaje1'], c)
            elif objeto in RECURSOS:
                self.Superficie.blit(RECURSOS[objeto], c)

    def buscarCuadro(self, x, y):
        for pos, objetos in self.juego.mapa.lista():
            c = Rect(pos.x*self.CUADRO_ANCHO,
                (pos.y*self.PISO_CUERPO),
                self.CUADRO_ANCHO, self.PISO_TOPE + self.PISO_CUERPO)
            if c.collidepoint(x, y):
                return pos
        else:
            return Pos(None, None)


if __name__ == '__main__':
    mapa = []
    [mapa.extend(fila) for fila in [[(x, y) for x in range(8)] for y in range(8)]]
    mapa = Mapa(mapa)
    for pos, objeto in mapa.items():
        mapa.colocar('piso', pos)

    i = Interfaz()
    i.start()
