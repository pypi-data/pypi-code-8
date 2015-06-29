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

from lua.lua_wrap import LuaState
from lua.lua_values import get_value, push_value


class LuaGlobalEnvironment(object):
    def __init__(self, lua_state):
        self.__dict__["_lua_state"] = lua_state

    def __getattr__(self, name):
        self._lua_state.lua_getglobal(name)
        value = get_value(self._lua_state, -1)
        self._lua_state.lua_pop(1)
        return value

    def __setattr__(self, name, value):
        push_value(self._lua_state, value)
        self._lua_state.lua_setglobal(name)

    def __delattr__(self, name):
        self.__setattr__(name, None)


class Lua(object):
    def __init__(self, do_libs=True):
        self._lua_state = LuaState.luaL_newstate()
        self._lua_state.luaL_openlibs()
        self._lua_globals = LuaGlobalEnvironment(self._lua_state)

    def do_file(self, filename):
        self._lua_state.luaL_dofile(filename)

    def do_string(self, string):
        self._lua_state.luaL_dostring(string)

    @property
    def globals_(self):
        return self._lua_globals

    def __del__(self):
        self._lua_state.lua_close()
