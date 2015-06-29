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
    tests = loader.loadTestsFromTestCase(LuaWrapTestCase)
    suite.addTests(tests)
    return suite

class LuaWrapTestCase(unittest.TestCase):
    def setUp(self):
        from lua.lua_wrap import LuaState, LuaTypes
        self.L = LuaState.luaL_newstate()
        self.lua_types = LuaTypes
        self.L.luaL_openlibs()

    def tearDown(self):
        self.L.lua_close()

    def testSimpleAssign(self):
        lua_code = "a=42"
        self.assertEqual(0, self.L.luaL_loadbuffer(lua_code, "line"))
        self.assertEqual(0, self.L.lua_pcall(0, 0, 0))
        self.L.lua_getglobal('a')
        self.assertEqual(self.lua_types.TNUMBER, self.L.lua_type(-1))
        self.assertEqual(42, self.L.lua_tointeger(-1))

    def testLuaLCheckOption(self):
        self.L.lua_pushstring("asdf")
        options = ['fdsa', 'asdf', 'qwer']
        self.assertEqual(self.L.luaL_checkoption(1, None, options), 1)
        self.L.lua_pushnil()
        self.assertEqual(self.L.luaL_checkoption(2, 'qwer', options), 2)

    def testReadFile(self):
        self.assertEqual(0, self.L.luaL_dofile("test/data/21443387.lua"))

        self.L.lua_getglobal('get_name')
        self.assertEqual(0, self.L.lua_pcall(0, 1, 0))
        self.assertEqual(self.lua_types.TSTRING, self.L.lua_type(-1))
        self.assertEqual("UNNAMED PUZZLE", self.L.lua_tostring(-1))

        self.L.lua_getglobal('get_description')
        self.assertEqual(0, self.L.lua_pcall(0, 1, 0))
        self.assertEqual(self.lua_types.TTABLE, self.L.lua_type(-1))
        self.L.lua_pushinteger(1)
        self.L.lua_gettable(-2)
        self.assertEqual(self.lua_types.TSTRING, self.L.lua_type(-1))
        self.assertEqual("DESCRIPTION LINE 1", self.L.lua_tostring(-1))
        self.L.lua_pushinteger(2)
        self.L.lua_gettable(-3)
        self.assertEqual(self.lua_types.TSTRING, self.L.lua_type(-1))
        self.assertEqual("DESCRIPTION LINE 2", self.L.lua_tostring(-1))

        self.L.lua_pushinteger(1)
        self.L.lua_setglobal('STREAM_INPUT')
        self.L.lua_getglobal('get_streams')
        self.assertEqual(0, self.L.lua_pcall(0, 1, 0))
        self.assertEqual(self.lua_types.TTABLE, self.L.lua_type(-1))
        self.L.lua_pushinteger(1)
        self.L.lua_gettable(-2)
        self.assertEqual(self.lua_types.TTABLE, self.L.lua_type(-1))
        self.L.lua_pushinteger(1)
        self.L.lua_gettable(-2)
        self.assertEqual(self.lua_types.TNUMBER, self.L.lua_type(-1))

    # TODO: Test sufficient for coverage
