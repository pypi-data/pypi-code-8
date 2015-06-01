#!/usr/bin/env python2
# -*- coding: utf-8 -*-

import os
from setuptools import setup

import voicecom

dir_path = os.path.dirname(os.path.realpath(__file__))
with open(os.path.join(dir_path, 'README.rst')) as readme:
    long_description = readme.read()

setup(
    name='VoiceCom',
    version=voicecom.__version__,
    description='An open source Voice-User-Interface (VUI)',
    long_description=long_description,
    license='MIT License',
    url='https://github.com/koehlja/VoiceCom',
    author='https://github.com/koehlja',
    packages=['voicecom'],
    entry_points={'console_scripts': ['voicecom = voicecom:run']},
    classifiers=[
        'Development Status :: 1 - Planning',
        'Intended Audience :: Developers',
        'Intended Audience :: End Users/Desktop',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.3',
        'Programming Language :: Python :: 2.4',
        'Programming Language :: Python :: 2.5',
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 2 :: Only',
        'Topic :: Utilities',
        'Topic :: Home Automation',
        'Topic :: Multimedia :: Sound/Audio :: Speech',
        'Topic :: Scientific/Engineering :: Human Machine Interfaces',
    ],
    keywords=['voice', 'speech', 'recognition', 'computer'],
)
