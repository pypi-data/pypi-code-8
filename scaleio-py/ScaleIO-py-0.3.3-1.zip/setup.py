#!/usr/bin/env python
# -*- coding: utf-8 -*-
from setuptools import find_packages
from distutils.core import setup

install_reqs =[
    'requests==2.5.1',
    'requests-toolbelt==0.3.1',
    'wsgiref==0.1'
    ]

setup(
    author='Magnus Nilsson',
    author_email='magnus@karabas.nu',
    name='ScaleIO-py',
    description='Python interface to ScaleIO 1.31+ REST API',
    version="0.3.3-1",
    url='https://github.com/swevm/scaleio-py/',
    license='Apache License',
    packages=find_packages(),

    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Topic :: Software Development :: Libraries',
        'Topic :: Software Development :: Libraries :: Python Modules',
    ],
    install_requires=install_reqs,
)