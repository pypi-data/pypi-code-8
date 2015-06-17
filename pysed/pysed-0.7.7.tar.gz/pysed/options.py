#!/usr/bin/env python
# -*- coding: utf-8 -*-

# main.py file is part of pysed.

# Copyright 2014-2015 Dimitris Zlatanidis <d.zlatanidis@gmail.com>
# All rights reserved.

# pysed is utility that parses and transforms text

# https://github.com/dslackw/pysed

# Pysed is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU General Public License for more details.
# You should have received a copy of the GNU General Public License
# along with this program. If not, see <http://www.gnu.org/licenses/>.

import sys
from pysed.__metadata__ import (
    __prog__,
    __email__,
    __version__,
    __license__,
)


def usage():
    """Print usage and exit
    """
    arguments = [
        "Usage: {0} [-h] [-v]".format(__prog__),
        "             [[-r] [-f] [-s] [-m] [-l] [-g] [-s] --write]"
    ]
    for arg in arguments:
        print("{0}".format(arg))


def helps():
    """Print help message and exit
    """
    arguments = [
        "Usage: %s [OPTION] {pattern} {repl} {lines/max/flag} "
        "[input-file]\n" % (__prog__),
        "{0} is utility that parses and transforms text\n".format(__prog__),
        "optional arguments:",
        "  -h, --help       Print this help message and exit",
        "  -v, --version    Print program version and exit",
        "  -r, --replace    Search and replace text",
        "  -f, --findall    Find all from pattern in text",
        "  -s, --search     Search for the first matching",
        "  -m, --match      Pattern matching in the beginning",
        "  -l, --lines      Search pattern and print lines",
        "  -g, --highlight  Highlight and print text",
        "  -t, --stat       Print text statistics",
        "      --write      Write changes to file\n"
    ]
    for arg in arguments:
        print("{0}".format(arg))
    sys.exit()


def version():
    """Print version and exit
    """
    print('version : {0}'.format(__version__))
    print('License : {0}'.format(__license__))
    print('Email   : {0}'.format(__email__))
    sys.exit()
