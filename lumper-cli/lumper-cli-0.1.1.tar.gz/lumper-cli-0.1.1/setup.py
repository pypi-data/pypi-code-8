#!/usr/bin/env python
# encoding: utf-8
from __future__ import absolute_import, print_function
from setuptools import find_packages
import os

try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup


__version__ = '0.1.1'
__author__ = 'Dmitry Orlov <me@mosquito.su>'


supports = {
    'install_requires': [
        'crew>=0.8.9',
    ]
}

setup(
    name='lumper-cli',
    version=__version__,
    author=__author__,
    author_email='me@mosquito.su',
    license="MIT",
    description="Command line util for Lumper",
    platforms="all",
    url="http://github.com/mosquito/lumper-cli",
    classifiers=[
        'Environment :: Console',
        'Programming Language :: Python',
    ],
    scripts=['bin/lumper-cli'],
    long_description=open('README.rst').read(),
    packages=find_packages(),
    **supports
)
