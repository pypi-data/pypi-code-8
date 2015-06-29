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
from lua._lua import ffi, lib

"""
This module provides:
* Object versions of lua_State and lua_Buffer
* Abstraction of stringification which includes generating ffi strings and
  providing string lengths where necessary
"""

def ffi_str(str_):
    """
    Only needs to be used if the argument is not `const char *`
    """
    return ffi.new("char[]", str_)


MULTRET = lib.LUA_MULTRET


class LuaPseudoIndices(object):
    LUA_REGISTRYINDEX = lib.LUA_REGISTRYINDEX
    LUA_ENVIRONINDEX = lib.LUA_ENVIRONINDEX
    LUA_GLOBALSINDEX = lib.LUA_GLOBALSINDEX


class LuaGCWhat(object):
    GCSTOP = lib.LUA_GCSTOP
    GCRESTART = lib.LUA_GCRESTART
    GCCOLLECT = lib.LUA_GCCOLLECT
    GCCOUNT = lib.LUA_GCCOUNT
    GCCOUNTB = lib.LUA_GCCOUNTB
    GCSTEP = lib.LUA_GCSTEP
    GCSETPAUSE = lib.LUA_GCSETPAUSE
    GCSETSTEPMUL = lib.LUA_GCSETSTEPMUL


class LuaError(object):
    ERRSYNTAX = lib.LUA_ERRSYNTAX
    ERRRUN = lib.LUA_ERRRUN
    ERRMEM = lib.LUA_ERRMEM
    ERRERR = lib.LUA_ERRERR


YIELD = lib.LUA_YIELD

class LuaTypes(object):
    TNONE = lib.LUA_TNONE
    TNIL = lib.LUA_TNIL
    TNUMBER = lib.LUA_TNUMBER
    TBOOLEAN = lib.LUA_TBOOLEAN
    TSTRING = lib.LUA_TSTRING
    TTABLE = lib.LUA_TTABLE
    TFUNCTION = lib.LUA_TFUNCTION
    TUSERDATA = lib.LUA_TUSERDATA
    TTHREAD = lib.LUA_TTHREAD
    TLIGHTUSERDATA = lib.LUA_TLIGHTUSERDATA


# TODO: Basically anything involving a lua_Alloc, lua_CFunction, lua_Reader,
# lua_Writer (aka the function pointer typedefs)
# TODO: Debug functions for same reason as above
# TODO: Convert certain values from C-esque types to pythonic types, for
# instance the return value of functions like lua_isboolean
class LuaState(object):
    def __init__(self, L):
        """
        Internal use only. Should be created by one of the static methods.
        L - a cffi wrapped lua_State pointer.
        """
        self.L = L

    # lua.h functions

    #TODO: lua_State *lua_newstate (lua_Alloc f, void *ud);

    # TODO: lua_CFunction lua_atpanic (lua_State *L, lua_CFunction panicf);
    # Also, determine if this is even useable, given that this function needs
    # to call setjmp

    def lua_call(self, nargs, nresults):
        lib.lua_call(self.L, nargs, nresults)

    def lua_checkstack(self, extra):
        return lib.lua_checkstack(self.L, extra)

    def lua_close(self):
        lib.lua_close(self.L)

    def lua_concat(self, n):
        lib.lua_concat(self.L, n)

    # TODO: int lua_cpcall (lua_State *L, lua_CFunction func, void *ud);

    def lua_createtable(self, narr, nrec):
        lib.lua_createtable(self.L, narr, nrec)

    # TODO: int lua_dump (lua_State *L, lua_Writer writer, void *data);

    def lua_equal(self, index1, index2):
        return lib.lua_equal(self.L, index1, index2)

    # TODO: Determine if this is valid or not, given the longjmp it's going to
    # perform
    def lua_error(self):
        return lib.lua_error()

    def lua_gc(self, what, data):
        """
        what - see LuaGCWhat
        """
        return lib.lua_gc(self.L, what, data)

    # TODO: lua_Alloc lua_getallocf (lua_State *L, void **ud);

    def lua_getfenv(self, index):
        return lib.lua_getfenv(self.L, index)

    def lua_getfield(self, index, k):
        lib.lua_getfield(self.L, index, k)

    def lua_getglobal(self, name):
        lib.lua_getglobal(self.L, name)

    def lua_getmetatable(self, index):
        return lib.lua_getmetatable(self.L, index)

    def lua_gettable(self, index):
        lib.lua_gettable(self.L, index)

    def lua_gettop(self):
        return lua_gettop(self.L)

    def lua_insert(self, index):
        lib.lua_insert(self.L, index)

    def lua_isboolean(self, index):
        return lib.lua_isboolean(self.L, index)

    def lua_iscfunction(self, index):
        return lib.lua_iscfunction(self.L, index)

    def lua_isfunction(self, index):
        return lib.lua_isfunction(self.L, index)

    def lua_islightuserdata(self, index):
        return lib.lua_islightuserdata(self.L, index)

    def lua_isnil(self, index):
        return lib.lua_isnil(self.L, index)

    def lua_isnone(self, index):
        return lib.lua_isnone(self.L, index)

    def lua_isnoneornil(self, index):
        return lib.lua_isnoneornil(self.L, index)

    def lua_isnumber(self, index):
        return lib.lua_isnumber(self.L, index)

    def lua_isstring(self, index):
        return lib.lua_isstring(self.L, index)

    def lua_istable(self, index):
        return lib.lua_istable(self.L, index)

    def lua_isthread(self, index):
        return lib.lua_isthread(self.L, index)

    def lua_isuserdata(self, index):
        return lib.lua_isuserdata(self.L, index)

    def lua_lessthan(self, index1, index2):
        return lib.lua_lessthan(self.L, index1, index2)

    #TODO: int lua_load (lua_State *L, lua_Reader reader, void *data,
    #                    const char *chunkname);

    def lua_newtable(self):
        return lib.lua_newtable(self.L)

    def lua_newthread(self):
        return lib.lua_newthread(self.L)

    def lua_newuserdata(self, size):
        return lib.lua_newuserdata(self.L, size)

    def lua_next(self, index):
        return lib.lua_next(self.L, index)

    def lua_objlen(self, index):
        return lib.lua_objlen(self.L, index)

    def lua_pcall(self, nargs, nresults, errfunc):
        return lib.lua_pcall(self.L, nargs, nresults, errfunc)

    def lua_pop(self, n):
        lib.lua_pop(self.L, n)

    def lua_pushboolean(self, b):
        lib.lua_pushboolean(self.L, b)

    # TODO: void lua_pushcclosure (lua_State *L, lua_CFunction fn, int n);
    # TODO: void lua_pushcfunction (lua_State *L, lua_CFunction f);
    # TODO: const char *lua_pushfstring (lua_State *L, const char *fmt, ...);

    def lua_pushinteger(self, n):
        lib.lua_pushinteger(self.L, n)

    def lua_pushlightuserdata(self, p):
        lib.lua_pushlightuserdata(self.L, p)

    def lua_pushlstring(self, s):
        lib.lua_pushlstring(self.L, s, len(s))

    def lua_pushnil(self):
        lib.lua_pushnil(self.L)

    def lua_pushnumber(self, n):
        lib.lua_pushnumber(self.L, n)

    def lua_pushstring(self, s):
        lib.lua_pushstring(self.L, s)

    def lua_pushthread(self):
        return lib.lua_pushthread(self.L)

    def lua_pushvalue(self, index):
        lib.lua_pushvalue(self.L, index)

    def lua_rawequal(self, index1, index2):
        return lib.lua_rawequal(self.L, index1, index2)

    def lua_rawget(self, index):
        lib.lua_rawget(self.L, index)

    def lua_rawgeti(self, index, n):
        lib.lua_rawgeti(self.L, index, n)

    def lua_rawset(self, index):
        lib.lua_rawset(self.L, index)

    def lua_rawseti(self, index, n):
        lib.lua_rawseti(self.L, index, n)

    # TODO: void lua_register (lua_State *L, const char *name, lua_CFunction f);

    def lua_remove(self, index):
        lib.lua_remove(self.L, index)

    def lua_replace(self, index):
        lib.lua_replace(self.L, index)

    def lua_resume(self, narg):
        return lib.lua_resume(self.L, narg)

    # TODO: void lua_setallocf (lua_State *L, lua_Alloc f, void *ud);

    def lua_setfenv(self, index):
        return lib.lua_setfenv(self.L, index)

    def lua_setfield(self, index, k):
        lib.lua_setfield(self.L, index, k)

    def lua_setglobal(self, name):
        lib.lua_setglobal(self.L, name)

    def lua_setmetatable(self, index):
        return lib.lua_setmetatable(self.L, index)

    def lua_settable(self, index):
        lib.lua_settable(self.L, index)

    def lua_settop(self, index):
        lib.lua_settop(self.L, index)

    def lua_status(self):
        return lib.lua_status(self.L)

    def lua_toboolean(self, index):
        return lib.lua_toboolean(self.L, index)

    # TODO: lua_CFunction lua_tocfunction (lua_State *L, int index);

    def lua_tointeger(self, index):
        return lib.lua_tointeger(self.L, index)

    def lua_tolstring(self, index, len_):
        """
        len_ is a pass by reference parameter, if you want the result, pass in a
        indexable, and the zeroth element will be set to the resulting length
        parameter
        """
        if len_ is None:
            ffi_len = ffi.NULL
        else:
            ffi_len = ffi.new("size_t *")

        result = lib.lua_tolstring(self.L, index, ffi_len)

        if len_ is not None:
            len_[0] = ffi_len[0]

        return ffi.string(result)

    def lua_tonumber(self, index):
        return lib.lua_tonumber(self.L, index)

    # TODO: const void *lua_topointer (lua_State *L, int index);

    def lua_tostring(self, index):
        return ffi.string(lib.lua_tostring(self.L, index))

    def lua_tothread(self, index):
        return LuaState(lib.lua_tothread, index)

    # TODO: void *lua_touserdata (lua_State *L, int index);

    def lua_type(self, index):
        return lib.lua_type(self.L, index)

    def lua_typename(self, tp):
        return ffi.string(lib.lua_typename(self.L, tp))

    def lua_xmove(self, other, n):
        """
        self is treated as the from lua_State, other as the to lua_State
        """
        lua.lua_xmove(self.L, other.L, n)

    def lua_yield(self, nresults):
        return lua_yield(self.L, nresults)


    # TODO: All the debug functions


    # lualib.h functions
    def luaopen_base(self):
        return lib.luaopen_base(self.L)

    def luaopen_table(self):
        return lib.luaopen_table(self.L)

    def luaopen_io(self):
        return lib.luaopen_io(self.L)

    def luaopen_os(self):
        return lib.luaopen_os(self.L)

    def luaopen_string(self):
        return lib.luaopen_string(self.L)

    def luaopen_math(self):
        return lib.luaopen_math(self.L)

    def luaopen_debug(self):
        return lib.luaopen_debug(self.L)

    def luaopen_package(self):
        return lib.luaopen_package(self.L)

    def luaL_openlibs(self):
        lib.luaL_openlibs(self.L)


    # lauxlib.h functions
    @staticmethod
    def luaL_newstate():
        return LuaState(lib.luaL_newstate())

    def luaL_argcheck(self, cond, narg, extramsg):
        lib.luaL_argcheck(self.L, cond, narg, extramsg)

    def luaL_argerror(self, narg, extramsg):
        return lib.luaL_argerror(self.L, narg, extramsg)

    def luaL_buffinit(self, buff):
        lib.luaL_buffinit(self.L, buff.B)

    def luaL_callmeta(self, obj, e):
        return lib.luaL_callmeta(self.L, obj, e)

    def luaL_checkany(self, narg):
        return lib.luaL_checkany(self.L, narg)

    def luaL_checkint(self, narg):
        return lib.luaL_checkint(self.L, narg)

    def luaL_checkinteger(self, narg):
        return lib.luaL_checkinteger(self.L, narg)

    def luaL_checklong(self, narg):
        return lib.luaL_checklong(self.L, narg)

    def luaL_checklstring(self, narg, len_):
        """
        len_ is a pass by reference parameter, if you want the result, pass in a
        indexable, and the zeroth element will be set to the resulting length
        parameter
        """
        if len_ is None:
            ffi_len = ffi.NULL
        else:
            ffi_len = ffi.new("size_t *")

        result = lib.luaL_checklstring(self.L, narg, ffi_len)

        if len_ is not None:
            len_[0] = ffi_len[0]

        return ffi.string(result)

    def luaL_checknumber(self, narg):
        return lib.luaL_checknumber(self.L, narg)

    def luaL_checkoption(self, narg, default, list_):
        """
        list_ - must be an iterable object
        """
        ffi_list = [ffi_str(_) for _ in list_]
        ffi_list.append(ffi.NULL)
        ffi_ffi_list = ffi.new("const char * const []", ffi_list)

        if default is None:
            default = ffi.NULL

        return lib.luaL_checkoption(self.L, narg, default, ffi_ffi_list)

    def luaL_checkstack(self, sz, msg):
        lib.luaL_checkstack(self.L, sz, msg)

    def luaL_checkstring(self, narg):
        return ffi.string(lib.luaL_checkstring(self.L, narg))

    def luaL_checktype(self, narg, t):
        lib.luaL_checktype(self.L, narg, t)

    # TODO: void *luaL_checkudata (lua_State *L, int narg, const char *tname);

    def luaL_dofile(self, filename):
        return lib.luaL_dofile(self.L, filename)

    def luaL_dostring(self, str_):
        return lib.luaL_dostring(self.L, str_)

    # TODO: int luaL_error (lua_State *L, const char *fmt, ...);

    def luaL_getmetafield(self, obj, e):
        return lib.luaL_getmetafield(self.L, obj, e)

    def luaL_getmetatable(self, tname):
        lib.luaL_getmetatable(self.L, tname)

    def luaL_gsub(self, s, p, r):
        return ffi.string(lib.luaL(self.L, s, p, r))

    def luaL_loadbuffer(self, buff, name):
        return lib.luaL_loadbuffer(self.L, buff, len(buff), name)

    def luaL_loadfile(self, filename):
        return lib.luaL_loadfile(self.L, filename)

    def luaL_loadstring(self, s):
        return lib.luaL_loadstrinig(self.L, s)

    def luaL_newmetatable(self, tname):
        return lib.luaL_newmetatable(self.L, tname)

    def luaL_optint(self, narg, d):
        return lib.luaL_optint(self.L, narg, d)

    def luaL_optinteger(self, narg, d):
        return lib.luaL_optinteger(self.L, narg, d)

    def luaL_optlong(self, narg, d):
        return lib.luaL_optlong(self.L, narg, d)

    def luaL_optlstring(self, narg, d, l):
        """
        l is a pass by reference parameter, if you want the result, pass in a
        indexable, and the zeroth element will be set to the resulting length
        parameter
        """
        if l is None:
            ffi_len = ffi.NULL
        else:
            ffi_len = ffi.new("size_t *")

        result = lib.luaL_optlstring(self.L, narg, d, ffi_len)

        if l is not None:
            l[0] = ffi_len[0]

        return ffi.string(result)

    def luaL_optnumber(self, narg, d):
        return lib.luaL_optnumber(self.L, narg, d)

    def luaL_optstring(self, narg, d):
        return ffi.string(lib.luaL_optstring(self.L, narg, d))

    def luaL_ref(self, t):
        return lib.luaL_ref(self.L, t)

    # TODO: void luaL_register (lua_State *L, const char *libname,
    #                           const luaL_Reg *l);

    def luaL_typename(self, index):
        return ffi.string(lib.luaL_typename(self.L, index))

    def luaL_typerror(self, narg, tname):
        return lib.luaL_typerror(self.L, narg, tname)

    def luaL_unref(self, t, ref):
        return lib.luaL_unref(self.L, t, ref)

    def luaL_where(self, lvl):
        return lib.luaL_where(self.L, lvl)


# TODO: Wrap the remaining function for things like buffers
