#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Copyright 2009-2015 Joao Carlos Roseta Matos
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

"""Application basic information."""

# Python 3 compatibility
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
# sometimes py2exe requires the following import to be commented
from __future__ import unicode_literals

import datetime as dt


APP_NAME = b'APPLICATION_NAME'
APP_VERSION = 'APPLICATION_VERSION'
LICENSE = 'APPLICATION_LICENSE'
AUTHOR = 'APPLICATION_AUTHOR'
AUTHOR_EMAIL = 'APPLICATION_EMAIL'
URL = 'APPLICATION_URL'
KEYWORDS = 'APPLICATION_KEYWORDS'

# check all below
CLASSIFIERS = ['Development Status :: 4 - Beta',
               'Environment :: Console',
               'Environment :: Win32 (MS Windows)',
               'Intended Audience :: Developers',
               'Natural Language :: English',
               'License :: OSI Approved ::' + ' ' + LICENSE,
               'Operating System :: OS Independent',
               'Programming Language :: Python',
               'Programming Language :: Python :: 2.7',
               'Programming Language :: Python :: 3.4',
               'Topic :: Other/Nonlisted Topic',
              ]

COPYRIGHT = 'Copyright 2009-' + str(dt.date.today().year) + ' '  + AUTHOR

APP_TYPE = 'application'  # it can be application or module

README_FILE = 'README.rst'
REQUIREMENTS_FILE = 'requirements.txt'
