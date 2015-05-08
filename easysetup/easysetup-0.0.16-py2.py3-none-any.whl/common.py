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

"""Common constants and functions."""

# Python 3 compatibility
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

import imp
import io  # Python 3 compatibility
import json
import os
import pickle as pkl
import sys
import time

# from builtins import input  # Python 3 compatibility

import appinfo
import localization as lcl


APP_INFO_FILENAME = 'appinfo.py'
PY = int(sys.version[0])

# set correct path to all data files
DATA_PATH = ''
# if current module is frozen, use exe path
if (hasattr(sys, 'frozen') or  # new py2exe
   hasattr(sys, 'importers') or  # old py2exe
   imp.is_frozen('__main__')):  # tools/freeze
    DATA_PATH = os.path.dirname(sys.executable.decode(lcl.UTF_ENC)) + os.sep
else:
    # use ...\site-packages\XXXXX\
    DATA_PATH = __file__.replace(__file__.split(os.sep)[-1], '')

LICENSE_FILE = DATA_PATH + 'LICENSE.txt'
DATA_FILE = DATA_PATH + 'data'
PKL_EXT = '.pkl'
JSON_EXT = '.json'

if lcl.LANG == 'PT':
    USAGE_FILE = DATA_PATH + 'usage_pt.txt'
else:
    USAGE_FILE = DATA_PATH + 'usage.txt'


def usage():
    """Returns usage text, read from a file."""
    if os.path.isfile(USAGE_FILE):  # if file exists
        with io.open(USAGE_FILE, encoding=lcl.UTF_ENC) as f_in:
            text = f_in.read()
    else:
        print(lcl.FILE_NOT_FOUND, USAGE_FILE)
        text = ''
    return text


def banner():
    """Returns banner text."""
    banner_txt = '\n' + appinfo.APP_NAME + lcl.VERSION_WITH_SPACES + \
                 appinfo.APP_VERSION + ', ' + appinfo.COPYRIGHT + '\n' + \
                 appinfo.APP_NAME + lcl.BANNER
    return banner_txt


def version():
    """Returns version."""
    return appinfo.APP_VERSION


def license_():
    """Returns license text, read from a file."""
    if os.path.isfile(LICENSE_FILE):  # if file exists
        with io.open(LICENSE_FILE, encoding=lcl.UTF_ENC) as f_in:
            text = f_in.read()
    else:
        print(lcl.FILE_NOT_FOUND, LICENSE_FILE)
        text = ''
    return text


def sleep(seconds=5):
    """Pause for specified time."""
    time.sleep(seconds)


def load_data(data_format=0):
    """Load data (list).

    data_format:
        0 = json
        1 = pickle
    """
    data_lst = []
    if data_format == 0:  # json
        data_file = DATA_FILE + JSON_EXT
        if os.path.isfile(data_file):  # if file exists
            with io.open(data_file, encoding=lcl.UTF_ENC) as f_in:
                data_lst = json.loads(f_in.read())
    elif data_format == 1:  # pkl
        data_file = DATA_FILE + PKL_EXT
        if os.path.isfile(data_file):  # if file exists
            with open(data_file, 'rb') as f_in:
                data_lst = pkl.load(f_in)
    else:
        # Error
        pass
    return data_lst


def save_data(data_lst, data_format=0):
    """Save data (list).

    data_format:
        0 = json
        1 = pickle
    """
    if data_format == 0:  # json
        with io.open(DATA_FILE + JSON_EXT, 'w', encoding=lcl.UTF_ENC) as f_out:
            f_out.write(json.dumps(data_lst, ensure_ascii=False))
    elif data_format == 1:  # pkl
        with open(DATA_FILE + PKL_EXT, 'wb') as f_out:
            pkl.dump(data_lst, f_out)
    else:
        # Error
        pass


if __name__ == '__main__':
    # import doctest
    # doctest.testmod(verbose=True)
    pass
