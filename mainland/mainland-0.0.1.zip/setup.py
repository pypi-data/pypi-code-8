# Copyright (c) Moshe Zadka
# See LICENSE for details.
from distutils import cmd, spawn

import os
import subprocess
import sys

import setuptools
import versioneer

import mainland as module

setuptools.setup(
    url='https://github.com/moshez/mainland',
    classifiers=[
        'Development Status :: 3 - Alpha',
        'License :: OSI Approved :: MIT License',
        'Operating System :: POSIX',
        'Topic :: System',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
    ],
    packages=setuptools.find_packages(),
    install_requires=['six >= 1.9.0', 'attrs'],
    version=versioneer.get_version(),
    cmdclass=versioneer.get_cmdclass(),
    **module.metadata
)
