#!/usr/bin/env python
# -*- coding: utf-8 -*-

from glob import glob
from os import path
try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup


dependency_links = [
    'git+https://github.com/chr15m/PodSixNet.git',
    ]

install_requires = [
    'pygame',
    'PodSixNet',
    'lxml',
    'weasyprint',
    ]

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
        'CambiosNoDeseados = Cambios.main:main',
        'Cambios-Servidor = Cambios.servidor:main'
        ],
    'gui_scripts': [
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
    version = '0.0.1dev3',
    license = 'MIT',
    author = 'Wolfang Torres',
    author_email='Wolfang.Torres@gmail.com',
    url = "https://bitbucket.org/WolfangT/cambiosnodeseadoscd",
    long_description = open('README.md').read(),

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
