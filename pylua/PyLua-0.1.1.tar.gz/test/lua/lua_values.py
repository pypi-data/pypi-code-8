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
    tests = loader.loadTestsFromTestCase(LuaTableTestCase)
    suite.addTests(tests)
    tests = loader.loadTestsFromTestCase(LuaFunctionTestCase)
    suite.addTests(tests)
    tests = loader.loadTestsFromTestCase(PushValueTestCase)
    suite.addTests(tests)
    tests = loader.loadTestsFromTestCase(RealCodeTestCase)
    suite.addTests(tests)
    return suite

lua_format_table = """
function format_table(t)
    result = "{"
    for key,value in pairs(t) do
        result = result.."["..tostring(key).."]="..tostring(value)..","
    end
    result = result.."}"
    return result
end
"""

class LuaTableTestCase(unittest.TestCase):
    def setUp(self):
        from lua.lua_values import LuaTable
        from lua.lua_wrap import LuaState, LuaTypes
        self.L = LuaState.luaL_newstate()
        self.lua_types = LuaTypes
        self.L.luaL_openlibs()
        self.lua_table = LuaTable

    def tearDown(self):
        self.L.lua_close()

    def testNewTable(self):
        table = self.lua_table.new_table(self.L)
        table["a"] = 2
        table["b"] = True
        table._push_self()
        self.assertEqual(self.lua_types.TTABLE, self.L.lua_type(-1))
        self.L.lua_pop(1)
        self.assertEqual(table["a"], 2.0)
        self.assertEqual(table["b"], True)
        self.assertEqual(0, self.L.luaL_dostring(lua_format_table))
        self.L.lua_getglobal("format_table")
        self.assertEqual(self.lua_types.TFUNCTION, self.L.lua_type(-1))
        table._push_self()
        self.assertEqual(0, self.L.lua_pcall(1, 1, 0))
        self.assertEqual("{[a]=2,[b]=true,}", self.L.lua_tostring(-1))

    def testTableFromIndex(self):
        table = self.lua_table.new_table(self.L)
        table["a"] = 2
        table["b"] = True
        table._push_self()
        table2 = self.lua_table(self.L, -1)
        self.assertEqual(table2["a"], 2.0)
        self.assertEqual(table2["b"], True)

    def testNewTableInit(self):
        table = self.lua_table.new_table(self.L, {'a': 2, 'b': True})
        self.assertEqual(table["a"], 2.0)
        self.assertEqual(table["b"], True)


class PushValueTestCase(unittest.TestCase):
    def setUp(self):
        from lua.lua_values import push_value
        from lua.lua_wrap import LuaState, LuaTypes
        self.L = LuaState.luaL_newstate()
        self.lua_types = LuaTypes
        self.L.luaL_openlibs()
        self.push_value = push_value

    def tearDown(self):
        self.L.lua_close()

    def testPushNone(self):
        self.push_value(self.L, None)
        self.assertEqual(self.lua_types.TNIL, self.L.lua_type(-1))
        self.L.lua_pop(1)

    def testPushInteger(self):
        self.push_value(self.L, 1)
        self.assertEqual(self.lua_types.TNUMBER, self.L.lua_type(-1))
        self.assertEqual(self.L.lua_tonumber(-1), 1.0)
        self.L.lua_pop(1)

    def testPushFloat(self):
        self.push_value(self.L, 1.5)
        self.assertEqual(self.lua_types.TNUMBER, self.L.lua_type(-1))
        self.assertEqual(self.L.lua_tonumber(-1), 1.5)
        self.L.lua_pop(1)

    def testPushBoolean(self):
        self.push_value(self.L, True)
        self.assertEqual(self.lua_types.TBOOLEAN, self.L.lua_type(-1))
        self.assertEqual(self.L.lua_toboolean(-1), True)
        self.L.lua_pop(1)

    def testPushString(self):
        self.push_value(self.L, "asdf")
        self.assertEqual(self.lua_types.TSTRING, self.L.lua_type(-1))
        self.assertEqual(self.L.lua_tostring(-1), "asdf")
        self.L.lua_pop(1)

    def testPushList(self):
        from lua.lua_values import LuaTable
        self.push_value(self.L, [1,2.5,True])
        self.assertEqual(self.lua_types.TTABLE, self.L.lua_type(-1))
        table = LuaTable(self.L, -1)
        self.assertEqual(table[1], 1)
        self.assertEqual(table[2], 2.5)
        self.assertEqual(table[3], True)

    def testPushDictionary(self):
        from lua.lua_values import LuaTable
        self.push_value(self.L, {1:2, "a": True, "c": "b"})
        self.assertEqual(self.lua_types.TTABLE, self.L.lua_type(-1))
        table = LuaTable(self.L, -1)
        self.assertEqual(table[1], 2)
        self.assertEqual(table['a'], True)
        self.assertEqual(table['c'], 'b')

    def testPushLuaValue(self):
        from lua.lua_values import LuaTable
        table = LuaTable.new_table(self.L, {1:2, "a": True, "c": "b"})
        self.push_value(self.L, table)
        self.assertEqual(self.lua_types.TTABLE, self.L.lua_type(-1))
        table2 = LuaTable(self.L, -1)
        self.assertEqual(table2[1], 2)
        self.assertEqual(table2['a'], True)
        self.assertEqual(table2['c'], 'b')


class LuaFunctionTestCase(unittest.TestCase):
    def setUp(self):
        from lua.lua_values import LuaTable
        from lua.lua_wrap import LuaState, LuaTypes
        self.L = LuaState.luaL_newstate()
        self.lua_types = LuaTypes
        self.L.luaL_openlibs()
        self.lua_table = LuaTable

    def tearDown(self):
        self.L.lua_close()

    def testNewTable(self):
        from lua.lua_values import LuaFunction
        table = self.lua_table.new_table(self.L)
        table["a"] = 2
        table["b"] = True
        self.assertEqual(0, self.L.luaL_dostring(lua_format_table))
        self.L.lua_getglobal("format_table")
        func = LuaFunction(self.L, -1)
        self.assertEqual("{[a]=2,[b]=true,}", func(table))


class RealCodeTestCase(unittest.TestCase):
    def setUp(self):
        from lua.lua_values import LuaTable
        from lua.lua_wrap import LuaState, LuaTypes
        self.L = LuaState.luaL_newstate()
        self.lua_types = LuaTypes
        self.L.luaL_openlibs()
        self.lua_table = LuaTable

    def tearDown(self):
        self.L.lua_close()

    def testCallStuff(self):
        from lua.lua_values import LuaFunction
        self.assertEqual(0, self.L.luaL_dofile("test/data/21443387.lua"))

        self.L.lua_getglobal('get_name')
        get_name = LuaFunction(self.L, -1)
        self.L.lua_getglobal('get_description')
        get_description = LuaFunction(self.L, -1)
        self.L.lua_getglobal('get_streams')
        get_streams = LuaFunction(self.L, -1)
        self.L.lua_getglobal('get_layout')
        get_layout = LuaFunction(self.L, -1)

        self.assertEqual("UNNAMED PUZZLE", get_name())
        description = get_description()
        self.assertEqual(description[1], "DESCRIPTION LINE 1")
        self.assertEqual(description[2], "DESCRIPTION LINE 2")

        STREAM_INPUT = 1
        STREAM_OUTPUT = 2
        TILE_COMPUTE = 3

        self.L.lua_pushinteger(STREAM_INPUT)
        self.L.lua_setglobal('STREAM_INPUT')
        self.L.lua_pushinteger(STREAM_OUTPUT)
        self.L.lua_setglobal('STREAM_OUTPUT')
        self.L.lua_pushinteger(TILE_COMPUTE)
        self.L.lua_setglobal('TILE_COMPUTE')

        streams = get_streams()
        self.assertEqual(streams[1][1], STREAM_INPUT)
        self.assertEqual(streams[1][2], "IN.A")
        self.assertEqual(streams[1][3], 1.0)
        self.assertEqual(streams[2][1], STREAM_OUTPUT)
        self.assertEqual(streams[2][2], "OUT.A")
        self.assertEqual(streams[2][3], 2.0)

        layout = get_layout()
        for i in xrange(1,13):
            self.assertEqual(layout[i], TILE_COMPUTE)

    # TODO: Test sufficient for coverage
