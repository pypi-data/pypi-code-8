#!/usr/bin/env python2
# -*- coding: utf-8 -*-

import os
from setuptools import setup

dir_path = os.path.dirname(os.path.realpath(__file__))
try:
    with open(os.path.join(dir_path, 'README.md')) as readme:
        long_description = readme.read()
except IOError:
    long_description = ''

setup(
    name='VoiceCom',
    version='0.0.2rc0',
    packages=['voicecom'],
    author='https://github.com/koehlja',
    url='https://github.com/koehlja/VoiceCom',
    license='MIT License',
    description='Voice User Interface',
    long_description=long_description,
    keywords='voice speech recognition computer',
    entry_points={'console_scripts': ['voicecom = voicecom.__main__:main']},
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
)
