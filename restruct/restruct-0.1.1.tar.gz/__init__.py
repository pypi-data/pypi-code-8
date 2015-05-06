
#
# ReStruct -- Turn SQL results into beautiful JSON structures.
#
# Copyright (c) 2015, Web Heroes Inc..
#
# ReStruct is free software: you can redistribute it and/or modify it under the
# terms of the GNU General Public License as published by the Free Software
# Foundation, either version 3 of the License, or (at your option) any later
# version.  See the LICENSE file at the top of the source tree.
#
# ReStruct is distributed in the hope that it will be useful, but WITHOUT ANY
# WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR
# A PARTICULAR PURPOSE.  See the GNU General Public License for more details.
#

__author__                      = "Matthew Brisebois"
__email__                       = "matthew@webheroes.ca"
__copyright__                   = "Copyright (c) 2015 Web Heroes Inc."
__license__                     = "Dual License: GPLv3 (or later) and Commercial (see LICENSE)"

__all__			= ["restruct"]


def fill(s, data):
    if s.startswith(':<'):
        return data.get( s[2:].strip() )
    
    v		= s.format(**data)
    if s.startswith(':'):
        try:
            v	= eval(v[1:])
        except Exception as e:
            v	= None
    return v
    
def restruct( data, columns ):

    if type(data) in [list, tuple]:
        return _attach_list(data, columns)
    
    result 		= []
    struct		= columns.copy()

    struct.pop('.key', None)
    struct.pop('.index', None)
    struct.pop('.single', None)

    if ".include" in struct:
        include		= struct.pop('.include')
        include.update(struct)
        struct		= include
    
    for k,v in struct.items():
        k		= fill(k, data)
        if v is True:
            struct[k]	= data[k]
        elif type(v) is dict:
            struct[k]	= restruct( data, v )
        elif type(v) in [str,unicode]:
            struct[k]	= fill(v, data)
        elif v == False:
            del struct[k]
        else:
            struct[k]	= None
    return struct

def _attach_list( rows, columns ):
    if columns.get('.key') is not None:
        return _attach_groups(rows, columns)

    struct		= columns.copy()
    if ".include" in struct:
        include		= struct.pop('.include')
        include.update(struct)
        struct		= include
        
    result		= []
    for row in rows:
        result.append( restruct( row, struct ) )
    return result

def extract_struct(path, data):
    segments		= path.split('.')
    for s in segments[:-1]:
        data		= data[s]
    s			= segments.pop()
    return data.copy().pop(s)

def path_assign(path, data1, data2):
    segments		= path.split('.')
    for s in segments[:-1]:
        data1		= data1[s]
    s			= segments.pop()
    data1[s]		= data2
    return data1

def _attach_groups(data, struct):
    gstruct		= struct.copy()
    sub_structs		= {}
    duplicates		= []
    gkey		= gstruct.pop('.key', None)
    gindex		= gstruct.pop('.index', True)
    gsingle		= gstruct.pop('.single', False)

    if type(gkey) is list:
        duplicates	= gkey[:]
        gkey		= duplicates.pop(0)

    for k in duplicates:
        sub_structs[k]	= extract_struct(k, gstruct)
        
    groups		= _group_data(data, gkey)
    gresult		= {}
    for key,rows in groups.items():
        gresult[key]		= restruct( rows[0], gstruct )
        for k in duplicates:
            path_assign(k, gresult[key], restruct(rows, sub_structs[k]))
            
    if gsingle is True:
        if len(gresult):
            k,gresult	= gresult.popitem()
        else:
            k,gresult	= None,{}
    elif gindex is False:
        gresult		= gresult.values()
            
    return gresult

def _group_data(data, gkey):
    """Separates the values of an iterable into groups based on the given
    key.  Incoming data must be an iterable with dicts as values.  The
    normal usage would be the rows returned from an SQL query.

    Data before grouping
    : ({ id: 1, value: ... }, { id: 1, value: ... }, { id: 2, value: ... },  ...)

    Using {id} as the key the formatted data would be
    : {
    :     "1": [{ id: 1, value: ... }, { id: 1, value: ... }],
    :     "2": [{ id: 2, value: ... }],
    :     ...
    : }

    """
    groups			= {}
    for d in data:
        k			= fill(gkey, d)
        if k == "None":
            continue
        if k not in groups:
            groups[k]		= []
        groups[k].append(d)
    return groups
    
