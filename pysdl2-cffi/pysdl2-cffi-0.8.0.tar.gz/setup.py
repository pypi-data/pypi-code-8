#!/usr/bin/env python

from setuptools import setup

import codecs
README = codecs.open('README.rst', encoding='utf-8').read()
CHANGES = codecs.open('CHANGES.rst', encoding='utf-8').read()

setup(name="pysdl2-cffi",
    version="0.8.0",
    packages=['sdl', '_sdl', '_sdl_image', '_sdl_mixer', '_sdl_ttf'],
    package_data={'_sdl' : ['sdl.h', 'defines.h']},
    setup_requires=["cffi>=1.1.0"],
    install_requires=['cffi>=1.1.0', 'apipkg'],
    extras_require={
        'build':['pycparser'],
        ':sys_platform=="win32"': ['sdl2_lib']
        },
    cffi_modules=[
        "_sdl/cdefs.py:ffi",
        "_sdl_image/cdefs.py:ffi",
        "_sdl_mixer/cdefs.py:ffi",
        "_sdl_ttf/cdefs.py:ffi",
        ],
    description="SDL2 wrapper with cffi",
    long_description=README + CHANGES,
    license="GPLv2+",
    classifiers=[
        "Programming Language :: Python :: 2.7",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.4",
        "License :: OSI Approved :: GNU General Public License v2 or later (GPLv2+)"
	],
    keywords=['sdl', 'cffi>=1.1'],
    author="Daniel Holth",
    author_email="dholth@fastmail.fm",
    url="https://bitbucket.org/dholth/pysdl2-cffi")
