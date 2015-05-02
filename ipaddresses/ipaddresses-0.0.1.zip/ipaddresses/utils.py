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

"""Utils library."""

# Python 3 compatibility
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

# import builtins  # Python 3 compatibility
# import future  # Python 3 compatibility
import imp
# import io  # Python 3 compatibility
import locale
import os
import sys


PY = int(sys.version[0])

# set correct path to all data files
DATA_PATH = ''
# if current module is frozen, use exe path
if (hasattr(sys, 'frozen') or  # new py2exe
   hasattr(sys, 'importers') or  # old py2exe
   imp.is_frozen('__main__')):  # tools/freeze
    if PY < 3:
        DATA_PATH = unicode(os.path.dirname(sys.executable),
                            sys.getfilesystemencoding())
    else:
        DATA_PATH = os.path.dirname(sys.executable)
    DATA_PATH += os.sep
else:
    # use ...\site-packages\XXXXX\
    DATA_PATH = __file__.replace(__file__.split(os.sep)[-1], '')


def sys_lang():
    """Get system language."""
    lang = locale.getdefaultlocale()
    # lang = 'EN'  # only for testing
    if 'pt_' in lang[0]:  # Portuguese
        return 'PT'
    else:  # English
        return 'EN'

LANG = sys_lang()


def run(win_cmd='', x_cmd=''):
    """Run OS command."""
    if sys.platform == 'win32':
        os.system(win_cmd)
    else:
        os.system(x_cmd)


if __name__ == '__main__':
    # import doctest
    # doctest.testmod(verbose=True)
    pass
