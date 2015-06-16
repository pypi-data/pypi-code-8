#!/usr/bin/env python

from setuptools import setup

setup(
    name='add_asts',
    author='Phil Rosenfield',
    author_email='philip.rosenfield@unipd.it',
    version='0.1',
    py_modules=['asts'],
    scripts=['asts'],
    install_requires=['astropy', 'matplotlib', 'numpy', 'scipy']
)