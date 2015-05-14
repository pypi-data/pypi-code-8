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

"""Shared constants and functions between CLI and GUI modules."""

# Python 3 compatibility
from __future__ import (absolute_import, division, print_function,
                        unicode_literals)

import datetime as dt
# import io  # Python 3 compatibility
import os

# from builtins import input  # Python 3 compatibility

import common


MAX_DAYS = 99
MAX_DAYS_STR = str(MAX_DAYS)


def update_file(childs, last_upd):
    """Update data file and log file.

    The log file creates an history to be used in the future.
    """
    if common.DATA_FORMAT == common.JSON:
        last_upd_str = str(last_upd)  # ISO format
        common.save_data([childs, last_upd_str])
    elif common.DATA_FORMAT == common.PKL:
        common.save_data([childs, last_upd])
    else:
        # error
        pass

    if common.LOG:
        if common.DATA_FORMAT == common.JSON:
            last_upd_str = str(last_upd)
            common.save_data([childs, last_upd_str], common.LOG_FILE)
        elif common.DATA_FORMAT == common.PKL:
            common.save_data([childs, last_upd], common.LOG_FILE)
        else:
            # error
            pass


def read_file():
    """Reads and returns childs and last_upd from the data file."""
    data_lst = common.load_data()
    if data_lst:
        if common.DATA_FORMAT == common.JSON:
            childs, last_upd_str = data_lst
            # mask is ISO format
            last_upd = dt.datetime.strptime(last_upd_str, '%Y-%m-%d').date()
        elif common.DATA_FORMAT == common.PKL:
            childs, last_upd = data_lst
        else:
            # error
            pass
    else:
        childs = None
        last_upd = None
    return childs, last_upd


def create_file():
    """Create new data file and log file."""
    # use lower case letters or names
    childs = {'t': 0, 's': 0}
    last_upd = dt.date.today()
    update_file(childs, last_upd)
    return childs, last_upd


def auto_upd_datafile(childs, last_upd):
    """Automatic update based on current date vs last update date."""
    right_now = dt.date.today()
    days_to_remove = (right_now - last_upd).days  # convert to days and assign
    for child in childs:
        childs[child] -= days_to_remove
        childs[child] = max(0, childs[child])
    update_file(childs, right_now)
    return right_now


def open_create_datafile():
    """Opens datafile if it exists, otherwise creates it."""
    if os.path.isfile(common.DATA_FILE):  # if file exists
        childs, last_upd = read_file()
    else:
        childs, last_upd = create_file()
    return childs, last_upd


if __name__ == '__main__':
    # import doctest
    # doctest.testmod(verbose=True)
    pass
