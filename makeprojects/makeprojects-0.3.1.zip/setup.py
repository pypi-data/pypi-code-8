#!/usr/bin/env python
# -*- coding: utf-8 -*-

#
# Build egg file
#

# Copyright 2013-2015 by Rebecca Ann Heineman becky@burgerbecky.com

# It is released under an MIT Open Source license. Please see LICENSE
# for license details. Yes, you can use it in a
# commercial title without paying anything, just give me a credit.
# Please? It's not like I'm asking you for money!

from setuptools import setup
from setuptools import find_packages

import makeprojects

#
# Use the readme as the long description
#

long_description = open('README.rst').read()

#
# Parms for setup
#

setup_args = dict(
	name="makeprojects",
	version=makeprojects.__version__,
	description=makeprojects.__summary__,
	long_description=long_description,
	author=makeprojects.__author__,
	author_email=makeprojects.__email__,
	url=makeprojects.__uri__,
	license=makeprojects.__license__,
	keywords="makeprojects xcode visual studio codeblocks watcom",
	platforms="any",
	classifiers="""\
Development Status :: 3 - Alpha
Environment :: Console
Intended Audience :: Developers
License :: OSI Approved :: MIT License
Operating System :: OS Independent
Natural Language :: English
Programming Language :: Python
Programming Language :: Python :: 2
Programming Language :: Python :: 3
Programming Language :: Python :: 2.3
Programming Language :: Python :: 2.4
Programming Language :: Python :: 2.5
Programming Language :: Python :: 2.6
Programming Language :: Python :: 2.7
Programming Language :: Python :: 3.0
Programming Language :: Python :: 3.1
Programming Language :: Python :: 3.2
Programming Language :: Python :: 3.3
Programming Language :: Python :: 3.4
Topic :: Software Development""".splitlines(),
	packages=['makeprojects']
)

#
# Actually perform the creation of the egg file
# by using setuptools
#

if __name__ == '__main__':
    setup(**setup_args)

