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

"""Common use constants and functions."""

# Python 3 compatibility
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

# import builtins  # Python 3 compatibility
# import future  # Python 3 compatibility
import imp
import io  # Python 3 compatibility
import os
import sys

import appinfo
import localization as lcl


PY = int(sys.version[0])

# set correct path to all data files
DATA_PATH = ''
# if current module is frozen, use exe path
if (hasattr(sys, 'frozen') or  # new py2exe
   hasattr(sys, 'importers') or  # old py2exe
   imp.is_frozen('__main__')):  # tools/freeze
    if PY < 3:
        DATA_PATH = unicode(os.path.dirname(sys.executable), 'latin_1')
    else:
        DATA_PATH = os.path.dirname(sys.executable)
    DATA_PATH += os.sep
else:
    # use ...\site-packages\XXXXX\
    DATA_PATH = __file__.replace(__file__.split(os.sep)[-1], '')

LICENSE_FILE = DATA_PATH + 'LICENSE.txt'

if lcl.LANG == 'PT':
    BANNER_FILE = DATA_PATH + 'banner_pt.txt'
    USAGE_FILE = DATA_PATH + 'usage_pt.txt'
else:
    BANNER_FILE = DATA_PATH + 'banner.txt'
    USAGE_FILE = DATA_PATH + 'usage.txt'


def usage():
    """Returns usage text, read from a file."""
    if os.path.isfile(USAGE_FILE):  # if file exists
        with io.open(USAGE_FILE,
                     encoding=sys.getfilesystemencoding()) as file_:
            text = file_.read()
    else:
        print(lcl.FILE_NOT_FOUND, USAGE_FILE)
        text = ''
    return text


def banner():
    """Returns banner text."""
    banner_txt = ('\n' + appinfo.APP_NAME + lcl.VERSION_WITH_SPACES +
                  appinfo.APP_VERSION + ', ' + appinfo.COPYRIGHT + '\n')
    if os.path.isfile(BANNER_FILE):  # if file exists
        with io.open(BANNER_FILE,
                     encoding=sys.getfilesystemencoding()) as file_:
            banner_txt += file_.read()
    else:
        print(lcl.FILE_NOT_FOUND, BANNER_FILE)
    return banner_txt


def version():
    """Returns version."""
    return appinfo.APP_VERSION


def license_():
    """Returns license text, read from a file."""
    if os.path.isfile(LICENSE_FILE):  # if file exists
        with io.open(LICENSE_FILE,
                     encoding=sys.getfilesystemencoding()) as file_:
            text = file_.read()
    else:
        print(lcl.FILE_NOT_FOUND, LICENSE_FILE)
        text = ''
    return text


if __name__ == '__main__':
    # import doctest
    # doctest.testmod(verbose=True)
    pass
