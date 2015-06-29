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

from cffi import FFI

ffi = FFI()
ffi.set_source("lua._lua",
               """
               #include <lua.h>
               #include <lauxlib.h>
               #include <lualib.h>
               """,
               libraries=['lua'])

lua_types = """
typedef struct lua_State lua_State;
typedef void* (*lua_Alloc) (void *ud, void *ptr, size_t osize, size_t nsize);
typedef int (*lua_CFunction) (lua_State *L);
typedef ptrdiff_t lua_Integer;
typedef double lua_Number;
typedef const char * (*lua_Reader) (lua_State *L, void *data, size_t *size);
typedef int (*lua_Writer) (lua_State *L, const void* p, size_t sz, void* ud);
"""

lua_constants = """
static const int LUA_REGISTRYINDEX;
static const int LUA_ENVIRONINDEX;
static const int LUA_GLOBALSINDEX;

static const int LUA_MULTRET;

static const int LUA_GCSTOP;
static const int LUA_GCRESTART;
static const int LUA_GCCOLLECT;
static const int LUA_GCCOUNT;
static const int LUA_GCCOUNTB;
static const int LUA_GCSTEP;
static const int LUA_GCSETPAUSE;
static const int LUA_GCSETSTEPMUL;

static const int LUA_ERRSYNTAX;
static const int LUA_ERRRUN;
static const int LUA_ERRMEM;
static const int LUA_ERRERR;

static const int LUA_YIELD;

static const int LUA_TNONE;
static const int LUA_TNIL;
static const int LUA_TNUMBER;
static const int LUA_TBOOLEAN;
static const int LUA_TSTRING;
static const int LUA_TTABLE;
static const int LUA_TFUNCTION;
static const int LUA_TUSERDATA;
static const int LUA_TTHREAD;
static const int LUA_TLIGHTUSERDATA;
"""

# This includes all the declared functions and all the documented function-like
# macros that aren't debug related
# Exception: lua_setlevel - declared function, marked as "hack" and not
#                           documented
# Exception: lua_pushliteral - documented function-like macro, only works if s
#                              is a literal string, by definition cffi won't be
#                              passing literals
# Exception: lua_pushvfstring - declared function, cffi seems to have trouble
#                               with va_list type?
lua_functions = """
lua_CFunction lua_atpanic (lua_State *L, lua_CFunction panicf);
void lua_call (lua_State *L, int nargs, int nresults);
int lua_checkstack (lua_State *L, int extra);
void lua_close (lua_State *L);
void lua_concat (lua_State *L, int n);
int lua_cpcall (lua_State *L, lua_CFunction func, void *ud);
void lua_createtable (lua_State *L, int narr, int nrec);
int lua_dump (lua_State *L, lua_Writer writer, void *data);
int lua_equal (lua_State *L, int index1, int index2);
int lua_error (lua_State *L);
int lua_gc (lua_State *L, int what, int data);
lua_Alloc lua_getallocf (lua_State *L, void **ud);
void lua_getfenv (lua_State *L, int index);
void lua_getfield (lua_State *L, int index, const char *k);
void lua_getglobal (lua_State *L, const char *name);
int lua_getmetatable (lua_State *L, int index);
void lua_gettable (lua_State *L, int index);
int lua_gettop (lua_State *L);
void lua_insert (lua_State *L, int index);
int lua_isboolean (lua_State *L, int index);
int lua_iscfunction (lua_State *L, int index);
int lua_isfunction (lua_State *L, int index);
int lua_islightuserdata (lua_State *L, int index);
int lua_isnil (lua_State *L, int index);
int lua_isnone (lua_State *L, int index);
int lua_isnoneornil (lua_State *L, int index);
int lua_isnumber (lua_State *L, int index);
int lua_isstring (lua_State *L, int index);
int lua_istable (lua_State *L, int index);
int lua_isthread (lua_State *L, int index);
int lua_isuserdata (lua_State *L, int index);
int lua_lessthan (lua_State *L, int index1, int index2);
int lua_load (lua_State *L, lua_Reader reader, void *data,
              const char *chunkname);
lua_State *lua_newstate (lua_Alloc f, void *ud);
void lua_newtable (lua_State *L);
lua_State *lua_newthread (lua_State *L);
void *lua_newuserdata (lua_State *L, size_t size);
int lua_next (lua_State *L, int index);
size_t lua_objlen (lua_State *L, int index);
int lua_pcall (lua_State *L, int nargs, int nresults, int errfunc);
void lua_pop (lua_State *L, int n);
void lua_pushboolean (lua_State *L, int b);
void lua_pushcclosure (lua_State *L, lua_CFunction fn, int n);
void lua_pushcfunction (lua_State *L, lua_CFunction f);
const char *lua_pushfstring (lua_State *L, const char *fmt, ...);
void lua_pushinteger (lua_State *L, lua_Integer n);
void lua_pushlightuserdata (lua_State *L, void *p);
void lua_pushlstring (lua_State *L, const char *s, size_t len);
void lua_pushnil (lua_State *L);
void lua_pushnumber (lua_State *L, lua_Number n);
void lua_pushstring (lua_State *L, const char *s);
int lua_pushthread (lua_State *L);
void lua_pushvalue (lua_State *L, int index);
//const char *lua_pushvfstring (lua_State *L, const char *fmt, va_list argp);
int lua_rawequal (lua_State *L, int index1, int index2);
void lua_rawget (lua_State *L, int index);
void lua_rawgeti (lua_State *L, int index, int n);
void lua_rawset (lua_State *L, int index);
void lua_rawseti (lua_State *L, int index, int n);
void lua_register (lua_State *L, const char *name, lua_CFunction f);
void lua_remove (lua_State *L, int index);
void lua_replace (lua_State *L, int index);
int lua_resume (lua_State *L, int narg);
void lua_setallocf (lua_State *L, lua_Alloc f, void *ud);
int lua_setfenv (lua_State *L, int index);
void lua_setfield (lua_State *L, int index, const char *k);
void lua_setglobal (lua_State *L, const char *name);
int lua_setmetatable (lua_State *L, int index);
void lua_settable (lua_State *L, int index);
void lua_settop (lua_State *L, int index);
int lua_status (lua_State *L);
int lua_toboolean (lua_State *L, int index);
lua_CFunction lua_tocfunction (lua_State *L, int index);
lua_Integer lua_tointeger (lua_State *L, int index);
const char *lua_tolstring (lua_State *L, int index, size_t *len);
lua_Number lua_tonumber (lua_State *L, int index);
const void *lua_topointer (lua_State *L, int index);
const char *lua_tostring (lua_State *L, int index);
lua_State *lua_tothread (lua_State *L, int index);
void *lua_touserdata (lua_State *L, int index);
int lua_type (lua_State *L, int index);
const char *lua_typename  (lua_State *L, int tp);
void lua_xmove (lua_State *from, lua_State *to, int n);
int lua_yield  (lua_State *L, int nresults);
"""

lua_debug_types = """
typedef struct lua_Debug {
  int event;
  const char *name;           /* (n) */
  const char *namewhat;       /* (n) */
  const char *what;           /* (S) */
  const char *source;         /* (S) */
  int currentline;            /* (l) */
  int nups;                   /* (u) number of upvalues */
  int linedefined;            /* (S) */
  int lastlinedefined;        /* (S) */
  char short_src[...];        /* (S) */
  ...;
} lua_Debug;
typedef void (*lua_Hook) (lua_State *L, lua_Debug *ar);
"""

lua_debug_constants = """
static const int LUA_HOOKCALL;
static const int LUA_HOOKRET;
static const int LUA_HOOKTAILRET;
static const int LUA_HOOKLINE;
static const int LUA_HOOKCOUNT;

static const int LUA_MASKCALL;
static const int LUA_MASKRET;
static const int LUA_MASKLINE;
static const int LUA_MASKCOUNT;
"""

lua_debug_functions = """
lua_Hook lua_gethook (lua_State *L);
int lua_gethookcount (lua_State *L);
int lua_gethookmask (lua_State *L);
int lua_getinfo (lua_State *L, const char *what, lua_Debug *ar);
const char *lua_getlocal (lua_State *L, lua_Debug *ar, int n);
int lua_getstack (lua_State *L, int level, lua_Debug *ar);
const char *lua_getupvalue (lua_State *L, int funcindex, int n);
int lua_sethook (lua_State *L, lua_Hook f, int mask, int count);
const char *lua_setlocal (lua_State *L, lua_Debug *ar, int n);
const char *lua_setupvalue (lua_State *L, int funcindex, int n);
"""

lua_lib_functions = """
int luaopen_base (lua_State *L);
int luaopen_table (lua_State *L);
int luaopen_io (lua_State *L);
int luaopen_os (lua_State *L);
int luaopen_string (lua_State *L);
int luaopen_math (lua_State *L);
int luaopen_debug (lua_State *L);
int luaopen_package (lua_State *L);
void luaL_openlibs (lua_State *L);
"""

lua_aux_types = """
typedef struct luaL_Buffer luaL_Buffer;
typedef struct luaL_Reg {
  const char *name;
  lua_CFunction func;
} luaL_Reg;
"""

lua_aux_constants = """
static const int LUA_ERRFILE;

static const int LUAL_BUFFERSIZE;

static const int LUA_NOREF;
static const int LUA_REFNIL;
"""

lua_aux_functions = """
void luaL_addchar (luaL_Buffer *B, char c);
void luaL_addlstring (luaL_Buffer *B, const char *s, size_t l);
void luaL_addsize (luaL_Buffer *B, size_t n);
void luaL_addstring (luaL_Buffer *B, const char *s);
void luaL_addvalue (luaL_Buffer *B);
void luaL_argcheck (lua_State *L, int cond, int narg, const char *extramsg);
int luaL_argerror (lua_State *L, int narg, const char *extramsg);
void luaL_buffinit (lua_State *L, luaL_Buffer *B);
int luaL_callmeta (lua_State *L, int obj, const char *e);
void luaL_checkany (lua_State *L, int narg);
int luaL_checkint (lua_State *L, int narg);
lua_Integer luaL_checkinteger (lua_State *L, int narg);
long luaL_checklong (lua_State *L, int narg);
const char *luaL_checklstring (lua_State *L, int narg, size_t *l);
lua_Number luaL_checknumber (lua_State *L, int narg);
int luaL_checkoption (lua_State *L, int narg, const char *def,
                      const char *const lst[]);
void luaL_checkstack (lua_State *L, int sz, const char *msg);
const char *luaL_checkstring (lua_State *L, int narg);
void luaL_checktype (lua_State *L, int narg, int t);
void *luaL_checkudata (lua_State *L, int narg, const char *tname);
int luaL_dofile (lua_State *L, const char *filename);
int luaL_dostring (lua_State *L, const char *str);
int luaL_error (lua_State *L, const char *fmt, ...);
int luaL_getmetafield (lua_State *L, int obj, const char *e);
void luaL_getmetatable (lua_State *L, const char *tname);
const char *luaL_gsub (lua_State *L, const char *s, const char *p,
                       const char *r);
int luaL_loadbuffer (lua_State *L, const char *buff, size_t sz,
                     const char *name);
int luaL_loadfile (lua_State *L, const char *filename);
int luaL_loadstring (lua_State *L, const char *s);
int luaL_newmetatable (lua_State *L, const char *tname);
lua_State *luaL_newstate (void);
int luaL_optint (lua_State *L, int narg, int d);
lua_Integer luaL_optinteger (lua_State *L, int narg, lua_Integer d);
long luaL_optlong (lua_State *L, int narg, long d);
const char *luaL_optlstring (lua_State *L, int narg, const char *d, size_t *l);
lua_Number luaL_optnumber (lua_State *L, int narg, lua_Number d);
const char *luaL_optstring (lua_State *L, int narg, const char *d);
char *luaL_prepbuffer (luaL_Buffer *B);
void luaL_pushresult (luaL_Buffer *B);
int luaL_ref (lua_State *L, int t);
void luaL_register (lua_State *L, const char *libname, const luaL_Reg *l);
const char *luaL_typename (lua_State *L, int index);
int luaL_typerror (lua_State *L, int narg, const char *tname);
void luaL_unref (lua_State *L, int t, int ref);
void luaL_where (lua_State *L, int lvl);
"""

ffi.cdef(lua_types + lua_constants + lua_functions +
         lua_debug_types + lua_debug_constants + lua_debug_functions +
         lua_lib_functions +
         lua_aux_types + lua_aux_constants + lua_aux_functions)
