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

from lua.lua_wrap import LuaTypes, LuaPseudoIndices
import numbers

# TODO: Implement user data parts
def get_value(lua_state, index):
    type_ = lua_state.lua_type(index)

    if type_ == LuaTypes.TNIL:
        return None
    elif type_ == LuaTypes.TNUMBER:
        return lua_state.lua_tonumber(index)
    elif type_ == LuaTypes.TBOOLEAN:
        return lua_state.lua_toboolean(index) != 0
    elif type_ == LuaTypes.TSTRING:
        return lua_state.lua_tostring(index)
    elif type_ == LuaTypes.TTABLE:
        return LuaTable(lua_state, index)
    elif type_ == LuaTypes.TFUNCTION:
        return LuaFunction(lua_state, index)
    elif type_ == LuaTypes.TUSERDATA:
        raise NotImplementedError
    elif type_ == LuaTypes.TTHREAD:
        return LuaThread(lua_state, index)
    elif type_ == LuaTypes.TLIGHTUSERDATA:
        raise NotImplementedError


def push_value(lua_state, value):
    if isinstance(value, LuaValue):
        value._push_self()
    elif value is None:
        lua_state.lua_pushnil()
    elif isinstance(value, bool):
        lua_state.lua_pushboolean(value)
    elif isinstance(value, numbers.Integral):
        lua_state.lua_pushinteger(value)
    elif isinstance(value, numbers.Real):
        lua_state.lua_pushnumber(value)
    elif isinstance(value, str):
        lua_state.lua_pushstring(value)
    elif LuaTable.is_table_like(value):
        table = LuaTable.new_table(lua_state, value)
        table._push_self()
    else:
        # TODO: Wrap it up in some nice light user data
        raise NotImplementedError


class LuaValue(object):
    def __init__(self, lua_state, index):
        self._lua_state = lua_state
        self._lua_state.lua_pushvalue(index)
        reg_idx = LuaPseudoIndices.LUA_REGISTRYINDEX
        self._ref_idx = self._lua_state.luaL_ref(reg_idx)

    def _push_self(self):
        self._lua_state.lua_rawgeti(LuaPseudoIndices.LUA_REGISTRYINDEX,
                                    self._ref_idx)


# TODO: Add functions to make fully dict-like
class LuaTable(LuaValue):
    def __init__(self, lua_state, index):
        super(LuaTable, self).__init__(lua_state, index)

    @staticmethod
    def is_table_like(thing):
        return hasattr(thing, 'iteritems') or hasattr(thing, '__iter__')

    @staticmethod
    def new_table(lua_state, init=None):
        lua_state.lua_newtable()
        table = LuaTable(lua_state, -1)
        if init is not None:
            if hasattr(init, 'iteritems'):
                items = init.iteritems()
            else:
                items = enumerate(iter(init), 1)

            for key, value in items:
                push_value(lua_state, key)
                push_value(lua_state, value)
                lua_state.lua_settable(-3)

        lua_state.lua_pop(1)
        return table

    def __getitem__(self, key):
        self._push_self()
        push_value(self._lua_state, key)
        self._lua_state.lua_gettable(-2)
        retval = get_value(self._lua_state, -1)
        self._lua_state.lua_pop(2)
        return retval

    def __delitem__(self, key):
        self[key] = None

    def __setitem__(self, key, value):
        self._push_self()
        push_value(self._lua_state, key)
        push_value(self._lua_state, value)
        self._lua_state.lua_settable(-3)
        self._lua_state.lua_pop(1)


class LuaFunction(LuaValue):
    def __init__(self, lua_state, index):
        super(LuaFunction, self).__init__(lua_state, index)

    def __call__(self, *args):
        self._push_self()
        for arg in args:
            push_value(self._lua_state, arg)
        # TODO: Throw exception if call fails
        self._lua_state.lua_pcall(len(args), 1, 0)
        retval = get_value(self._lua_state, -1)
        self._lua_state.lua_pop(1)
        return retval


class LuaThread(LuaValue):
    def __init__(self, lua_state, index):
        super(LuaThread, self).__init__(lua_state, index)
