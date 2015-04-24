#!/usr/bin/env python

from setuptools import *

setup(
    name='uwaterloo-addcourse',
    version='0.0.13',
    license='GPLv3+',
    packages=['addcourse'],
    entry_points={
        'console_scripts': [
            'addcourse = addcourse:main',
        ],
    },
    install_requires=[
        'beautifulsoup4>=4.2.0',
    ],
)
