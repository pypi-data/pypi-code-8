# -*- coding: utf-8 -*-
#
# MONK Automated Development Environment Tooling
#
# Copyright (C) 2015 DResearch Fahrzeugelektronik GmbH
#
# This program is free software; you can redistribute it and/or
# modify it under the terms of the GNU General Public License
# as published by the Free Software Foundation; either version
# 2 of the License, or (at your option) any later version.
#

import os
import sys

try:
    from setuptools import setup
except ImportError as error:
    from distutils.core import setup

if sys.argv[-1] == 'publish':
    sys.argv = [sys.argv[0], 'sdist', 'bdist_wheel', 'upload']


def read(name):
    try:
        with open(name, 'r') as f:
            return f.read()
    except IOError:
        return ""

project = "monk_de"
version = "0.3.1"
setup(
    name=project,
    version=version,
    description = "Tmuxinator like tooling in python",
    author = "DResearch Fahrzeugelektronik GmbH",
    author_email = "project-monk@dresearch-fe.de",
    url="https://github.com/DFE/monk_de",
    py_modules = [project],
    license=read("LICENSE.txt"),
    entry_points = {
        'console_scripts' : [
            'mde = monk_de:main',
        ],
    },
    install_requires = [
    ],provides = [
        "{} ({})".format(project, version),
    ],
)
