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
    tests = loader.loadTestsFromTestCase(LuaCFFITestCase)
    suite.addTests(tests)
    return suite

class LuaCFFITestCase(unittest.TestCase):
    def setUp(self):
        from lua._lua import ffi, lib
        self.ffi = ffi
        self.lib = lib

    def testSimpleAssign(self):
        lua_code = "a=1"
        ffi_lua_code = self.ffi.new("char[]", lua_code)
        L = self.lib.luaL_newstate()
        self.lib.luaL_openlibs(L)
        retval = self.lib.luaL_loadbuffer(L, ffi_lua_code, len(lua_code), 
                                          self.ffi.new("char[]", "line"))
        self.assertEqual(0, retval);
        retval = self.lib.lua_pcall(L, 0, 0, 0)
        self.assertEqual(0, retval);

        self.lib.lua_close(L)
