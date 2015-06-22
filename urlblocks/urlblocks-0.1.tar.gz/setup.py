#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os

from setuptools import setup, find_packages

version = '0.1'

description = ('urlblocks is the module provided URL string class which can '
               'be operated as a constructor, consisting of some blocks - URL components.')


def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()

long_description = read('README.rst')



setup(
    name='urlblocks',
    author='Vladimir Chub',
    version=version,
    description=description,
    author_email="vartagg@users.noreply.github.com",
    url='http://github.com/vartagg/urlblocks',
    packages=find_packages(exclude=('test',)),
    classifiers=[
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 3',
    ],
)
