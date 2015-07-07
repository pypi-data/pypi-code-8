#!/usr/bin/env python
__version__ = '0.1'
__author__ = 'Richard Hoop'

import sys


try:
    from setuptools import setup
except ImportError:
    print("python-simpledaemon needs setuptools in order to build. Install it using"
          " your package manager (usually python-setuptools) or via pip (pip"
          " install setuptools).")
    sys.exit(1)

setup(
    name='python-simpledaemon',
    version=__version__,
    description='Easy Python Daemon',
    author=__author__,
    author_email='richard@projecticeland.net',
    license='GPLv3',
    data_files=[],
    url="https://github.com/gemini/python-simpledaemon",
    packages=['simpledaemon']
)
