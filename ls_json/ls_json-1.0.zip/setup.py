###############################################################
# -*- coding: utf-8 -*-
#!/usr/bin/env python
#
#  Copyright (c) 2015, alelec
#  https://www.alelec.net
#
#  This file is part of ls_json
#
# ls_json is free software; you can redistribute it and/or modify
# it under the terms of the PSF License as published by
# the Python Software Foundation; either version 2 of the License, or
# (at your option) any later version.
#
# ls_json is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the PSF License
# along with ls_json.  If not, see <https://docs.python.org/2/license.html>
import os
from setuptools import setup

def read(fname, skiplines=0):
    f = open(os.path.join(os.path.dirname(__file__), fname)).readlines()
    return "".join(f[skiplines:])

setup(name='ls_json',
    version = "1.0",
    py_modules = ['ls_json'],
    entry_points = {
          'console_scripts': [
              'ls_json = ls_json:main',                  
          ],              
      },
    # metadata for upload to PyPI
    author = "Andrew Leech",
    author_email = "andrew@alelec.net",
    description = "ls_json traverses either the provided path or current dir and returns the file tree (with file sizes) in json format",
    long_description = read('README.rst', 4),
    license = "PSF",
    keywords = "directory tree json",
    url = "https://github.com/andrewleech/ls_json"
)
