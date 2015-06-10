#!/usr/bin/env python
# -*- coding: utf-8 -*-

from glob import glob
from os import path
try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup


long_description = """
# README #


## ¿Que es Cambios No Deseados? ##

Es un proyecto entre unos amigos para crear una combinación entre un Rouge-Like y un TGC

Actualmente esta en la versión <a1> "alpha 1"


## ¿Como lo pruebo? ##

Por los momentos no existen un instalador


## ¿Como esta siendo desarrollado? ##

El juego esta escrito en python usando la librería PyGame para los gráficos y PodSixNet para la comunicación en red. El juego esta diseñado con un modelo servidor - cliente en mente.

El código esta estructurado en varios módulos que contienen un nivel de abstracción lógica diferente:

### Juego ###
Contiene las definiciones de los componentes del juego en si, que es un mapa, que es un personaje, etc.

### Cartas ###
Define el concepto de carta y maso, permite crear cartas en base a archivos xml

### Reglas ###
Contiene las definiciones de la forma en que el juego es jugado, los jugadores, interpreta los efectos de las cartas

### Interfaz ###
Crea la interfaz gráfica con la que el usuario interactúa

### Cliente ###
Define a un jugador que se conecta a un servidor para jugar, le permite a la interfaz enviar y recibir información

### Servidor ###
Define al servidor central que controla el juego, decide que información enviá a los clientes


## ¿Quien trabaja en esto? ##

El administrador es Wolfang Torres, lo puedes encontrar en wolfang.torres@gmail.com"""


dependency_links = [
    'https://github.com/chr15m/PodSixNet/tarball/master#egg=PodSixNet-78',
    'hg+https://bitbucket.org/pygame/pygame#egg=pygame-1.9.2a0',
    ]

install_requires = [
    'pygame',
    'PodSixNet',
    ]

extras_require = {
    'GeneracionCartas':  ['weasyprint', 'lxml'],
    }

py_modules = [
    ]

packages = [
    'Cambios',
    'Cambios.Habilidades',
    ]

package_dir = {
    'Cambios':path.join('src','Cambios'),
    }

package_data = {
    'Cambios':[
        path.join('Arte', '*.png'),
        path.join('Logs', '*.conf'),
        path.join('Cartas', '*.xml'),
        path.join('Estilos', '*'),
        path.join('Iconos', '*.png'),
        path.join('Letras', '*.otf'),
        path.join('Mapas', '*'),
        path.join('PreGeneradas', '*.png'),
        path.join('Recursos', '*.png'),
        ]
    }

data_files = [
    ]

scripts = [
    'script/Servidor',
    'script/Cliente',
    ]

entry_points = {
    'console_scripts': [
        'Cambios-Servidor = Cambios.servidor:main',
        ],
    'gui_scripts': [
        'CambiosNoDeseados = Cambios.cliente:main',
        ],
    }

classifiers=[
    # How mature is this project? Common values are
    #   3 - Alpha
    #   4 - Beta
    #   5 - Production/Stable
    'Development Status :: 2 - Pre-Alpha',

    # Indicate who your project is intended for
    'Intended Audience :: Gamers',
    'Topic :: Games/Entertainment'
    'Topic :: Games/Entertainment :: Turn Based Strategy'
    'Topic :: Games/Entertainment :: Simulation'

    # Pick your license as you wish (should match "license" above)
     'License :: OSI Approved :: MIT License',

    'Natural Language :: Spanish'
    # Specify the Python versions you support here. In particular, ensure
    # that you indicate whether you support Python 2, Python 3 or both.
    'Programming Language :: Python :: 2 :: Only',
    'Programming Language :: Python :: 2.7',
]


setup(
    name = 'CambiosNoDeseados',
    description = 'Cambios No Deseados - Conbinación de un RPG Tactico y un TCG',
    version = '0.0.2',
    license = 'MIT',
    author = 'Wolfang Torres',
    author_email='Wolfang.Torres@gmail.com',
    url = "https://bitbucket.org/WolfangT/cambiosnodeseadoscd",
    long_description = long_description,
    classifiers=classifiers,

    dependency_links = dependency_links,
    install_requires = install_requires,
    py_modules = py_modules,
    packages = packages,
    package_dir = package_dir,
    package_data = package_data,
    data_files = data_files,
    scripts = scripts,
    entry_points = entry_points,
    )
