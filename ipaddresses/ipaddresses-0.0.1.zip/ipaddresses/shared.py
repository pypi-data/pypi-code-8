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

"""Shared constants and functions."""

# Python 3 compatibility
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals
from future.moves.urllib.request import urlopen

# import builtins  # Python 3 compatibility
# import future  # Python 3 compatibility
import io  # Python 3 compatibility
import socket
import sys

import appinfo
import localization as lcl
import utils


LICENSE_FILE = utils.DATA_PATH + 'LICENSE.txt'

if utils.LANG == 'PT':
    BANNER_FILE = utils.DATA_PATH + 'banner_pt.txt'
    USAGE_FILE = utils.DATA_PATH + 'usage_pt.txt'
else:
    BANNER_FILE = utils.DATA_PATH + 'banner.txt'
    USAGE_FILE = utils.DATA_PATH + 'usage.txt'


def usage():
    """Returns usage text, read from a file."""
    with io.open(USAGE_FILE, encoding=sys.getfilesystemencoding()) as file_:
        text = file_.read()
    return text


def banner():
    """Returns banner text."""
    banner_txt = ('\n' + appinfo.APP_NAME + lcl.VERSION_WITH_SPACES +
                  appinfo.APP_VERSION + ', ' + appinfo.COPYRIGHT + '\n')
    with io.open(BANNER_FILE, encoding=sys.getfilesystemencoding()) as file_:
        banner_txt += file_.read()
    return banner_txt


def version():
    """Returns version."""
    return appinfo.APP_VERSION


def license_():
    """Returns license text, read from a file."""
    with io.open(LICENSE_FILE, encoding=sys.getfilesystemencoding()) as file_:
        text = file_.read()
    return text


def get_private_ip():
    """Get private IP address."""
    return socket.gethostbyname(socket.gethostname())


def get_public_ip():
    """Get public IP address."""
    data = str(urlopen('http://www.realip.info/api/p/realip.php').read())
    return data.split('"')[3]


if __name__ == '__main__':
    # import doctest
    # doctest.testmod(verbose=True)
    pass
