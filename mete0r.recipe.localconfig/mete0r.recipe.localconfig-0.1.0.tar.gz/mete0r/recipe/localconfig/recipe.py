# -*- coding: utf-8 -*-
#
#   mete0r.recipe.localconfig : override default config with local files
#   Copyright (C) 2015 mete0r <mete0r@sarangbang.or.kr>
#
#   This program is free software: you can redistribute it and/or modify
#   it under the terms of the GNU Lesser General Public License as published by
#   the Free Software Foundation, either version 3 of the License, or
#   (at your option) any later version.
#
#   This program is distributed in the hope that it will be useful,
#   but WITHOUT ANY WARRANTY; without even the implied warranty of
#   MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#   GNU Lesser General Public License for more details.
#
#   You should have received a copy of the GNU Lesser General Public License
#   along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
from __future__ import absolute_import
from __future__ import unicode_literals
import json
import os.path

from zc.buildout import UserError


class Recipe:

    def __init__(self, buildout, name, options):
        path = options['localconfig.path']
        required = options.get('localconfig.required', 'false')
        required = boolish(required)

        if not os.path.exists(path):
            if not required:
                return
            else:
                raise UserError('{} not found'.format(path))

        with open(path) as f:
            options_from_file = json.load(f)

        protected = (
            'recipe',
            'localconfig.path',
            'localconfig.required'
        )
        for k in options_from_file:
            if (k in options) and (k not in protected):
                v = options_from_file[k]

                # zc.buildout.buildout.Options require string values
                # Python 2.x: str (not unicode)
                # Python 3.x: str (=unicode)
                v = make_option_value(v)

                options[k] = v

    def install(self):
        return tuple()

    def update(self):
        return tuple()


def make_option_value(unicodevalue):
    ''' Make option value

    zc.buildout.buildout.Options require string values

    Python 2.x: str (not unicode)
    Python 3.x: str (=unicode)
    '''
    try:
        unicode
    except NameError:
        return unicodevalue
    if isinstance(unicodevalue, unicode):
        return unicodevalue.encode('utf-8')


def boolish(value):
    s = value.lower()

    for false in 'false', 'no', 'n', '0':
        if s == false:
            return False
    for true in 'true', 'yes', 'y', '1':
        if s == true:
            return True
    raise ValueError(value)
