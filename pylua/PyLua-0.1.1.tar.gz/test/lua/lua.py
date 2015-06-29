# Copyright 2015 Alex Orange
# 
# This file is part of PyLua.
# 
# PyLua is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
# 
# PyLua is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.
# 
# You should have received a copy of the GNU Affero General Public License
# along with PyLua.  If not, see <http://www.gnu.org/licenses/>.

from __future__ import absolute_import

import unittest

def load_tests(loader, tests, pattern):
    suite = unittest.TestSuite()
    tests = loader.loadTestsFromTestCase(RealCodeTestCase)
    suite.addTests(tests)
    return suite


class RealCodeTestCase(unittest.TestCase):
    def setUp(self):
        from lua.lua import Lua
        self.L = Lua()
        self.L.do_file("test/data/21443387.lua")

    def tearDown(self):
        del self.L

    def testCallStuff(self):
        self.assertEqual("UNNAMED PUZZLE", self.L.globals_.get_name())
        description = self.L.globals_.get_description()
        self.assertEqual(description[1], "DESCRIPTION LINE 1")
        self.assertEqual(description[2], "DESCRIPTION LINE 2")

        STREAM_INPUT = 1
        STREAM_OUTPUT = 2
        TILE_COMPUTE = 3

        self.L.globals_.STREAM_INPUT = STREAM_INPUT
        self.L.globals_.STREAM_OUTPUT = STREAM_OUTPUT
        self.L.globals_.TILE_COMPUTE = TILE_COMPUTE

        streams = self.L.globals_.get_streams()
        self.assertEqual(streams[1][1], STREAM_INPUT)
        self.assertEqual(streams[1][2], "IN.A")
        self.assertEqual(streams[1][3], 1.0)
        self.assertEqual(streams[2][1], STREAM_OUTPUT)
        self.assertEqual(streams[2][2], "OUT.A")
        self.assertEqual(streams[2][3], 2.0)

        layout = self.L.globals_.get_layout()
        for i in xrange(1,13):
            self.assertEqual(layout[i], TILE_COMPUTE)

    # TODO: Test sufficient for coverage

