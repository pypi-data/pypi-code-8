#!/usr/bin/env python

from setuptools import *
import addcourse

setup(
    name='uwaterloo-addcourse',
    version='0.0.8',
    license='GPLv3+',
    scripts=['addcourse.py'],

    install_requires=[
        'beautifulsoup4>=4.2.0',
    ],
)
