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

from unittest import TestCase
from unittest import makeSuite
import json
import os.path


class RecipeTest(TestCase):

    def test_read_json(self):
        from zc.buildout.buildout import Options
        from ..recipe import Recipe

        localconfig = {
            'foo': 'local-hello',
            'bar': 'local-world',
        }
        d = self.id()
        if not os.path.exists(d):
            os.mkdir(d)
        path = os.path.join(d, 'localconfig.json')
        with open(path, 'w') as f:
            json.dump(localconfig, f)

        options = Options(None, None, {
            'recipe': 'mete0r.recipe.localconfig',
            'localconfig.path': path,
            'foo': 'hello',
        })

        Recipe({}, 'config', options)

        self.assertEquals({
            'recipe': 'mete0r.recipe.localconfig',
            'localconfig.path': path,
            'foo': 'local-hello',
        }, options)

    def test_without_localconfig(self):
        from zc.buildout.buildout import Options
        from ..recipe import Recipe

        path = 'non-existing-file'

        options = Options(None, None, {
            'recipe': 'mete0r.recipe.localconfig',
            'localconfig.path': path,
            'foo': 'hello',
        })

        Recipe({}, 'config', options)
        self.assertEquals({
            'recipe': 'mete0r.recipe.localconfig',
            'localconfig.path': path,
            'foo': 'hello',
        }, options)

    def test_required(self):
        from zc.buildout import UserError
        from zc.buildout.buildout import Options
        from ..recipe import Recipe

        path = 'non-existing-file'

        options = Options(None, None, {
            'recipe': 'mete0r.recipe.localconfig',
            'localconfig.path': path,
            'localconfig.required': 'true',
            'foo': 'hello',
        })
        self.assertRaises(UserError, Recipe, {}, 'config', options)


def test_suite():
    return makeSuite(RecipeTest)
