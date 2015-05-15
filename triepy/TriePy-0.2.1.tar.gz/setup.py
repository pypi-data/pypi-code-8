#!/usr/bin/env python

import os
from setuptools import setup, find_packages


def _read(filename):
    """
    Reads a file

    Keyword arguments:
    filename -- the file to be read
    """
    return open(os.path.join(os.path.dirname(__file__), filename)).read()

setup(
    name='TriePy',
    version='0.2.1',
    packages=find_packages(),
    description='Simple Python Trie Data Structure',
    author='Adrian Cruz',
    author_email='drincruz@gmail.com',
    license='MIT',
    long_description=_read('README.md')
)
