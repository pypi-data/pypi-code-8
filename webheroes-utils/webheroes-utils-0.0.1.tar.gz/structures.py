
#
# WebHeroes-Utils -- Web Heroes Inc. python utility module
#
# Copyright (c) 2015, Web Heroes Inc..
#
# WebHeroes-Utils is free software: you can redistribute it and/or modify it
# under the terms of the GNU General Public License as published by the Free
# Software Foundation, either version 3 of the License, or (at your option) any
# later version.  See the LICENSE file at the top of the source tree.
#
# WebHeroes-Utils is distributed in the hope that it will be useful, but WITHOUT
# ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS
# FOR A PARTICULAR PURPOSE.  See the GNU General Public License for more
# details.
#

__author__                      = "Matthew Brisebois"
__email__                       = "matthew@webheroes.ca"
__copyright__                   = "Copyright (c) 2015 Web Heroes Inc."
__license__                     = "Dual License: GPLv3 (or later) and Commercial (see LICENSE)"

__all__				= ["endpoint"]

from .		import formatter, logging
import json, math

log			= logging.getLogger('structures')
log.setLevel(logging.DEBUG)

tables			= None
api_endpoints		= None

def endpoint(path, joins=True, index=True, single=False):
    global tables, api_endpoints
    
    with open('./json/tables.json', 'r') as f:
        tables		= json.loads(f.read())
    with open('./json/endpoints.json', 'r') as f:
        api_endpoints	= json.loads(f.read())
    
    segs		= path.strip('/').split('/')
    rules		= {}
    if len(segs) == 2 and segs[0] == "__raw__":
        table		= segs[1]
    else:    
        data		= api_endpoints
        for s in segs:
            data	= data.get(s)
            if data is None:
                raise Exception("Endpoint does not exist: {0}".format(path))
            
        rules		= data.get('.rules')
        log.debug(".rules: %s", json.dumps(rules, indent=4) )
        if rules is None:
            raise Exception("No rules at endpoint: {0}".format(path))
        
        table		= rules.get('table')
        if table is None:
            raise Exception("No table in rules at endpoint: {0}".format(path))

    table_set	= query_set(
        table,
        joins			= joins,
        index			= index,
        single			= single,
        structure		= rules.get('structure'),
        structure_update	= rules.get('structure_update'),
    )
    if rules.get('joins'):
        for key,join in rules.get('joins').items():
            table_set.join(key,join)
            
    if rules.get('includes'):
        for key,join in rules.get('includes').items():
            table_set.join(key, join, single=True)
            
    return table_set

def get_structure( table ):
    return tables.get(table, {}).get('structure', {})

def get_joins( table1, table2 ):
    joins		= tables.get(table2, {}).get('join_to', {}).get(table1)
    if joins is None:
        raise Exception("No join definition for {0} joining to {1}".format(table2, table1))
    return joins if type(joins) is list else [joins]

def get_columns( table, alias=None ):
    columns		= tables.get(table, {}).get('columns')
    if columns is None:
        return {}

    oalias		= alias or table
    
    column_dict		= {}
    for column, column_alias in columns.items():
        alias		= oalias
        if column.find('.') >= 0:
            if column.count('.') == 1:
                alias,column	= map(lambda x: x.strip('`'), column.split('.'))
            else:
                raise Exception("Unparsable column definition: %s", column)
        k		= "{0}.{1}".format(alias,column)
        log.error("Alias and column:  %s, %s", alias, column )
        real_column	= "`{0}`.`{1}`".format(alias, column)
        tabs		= max(0, 7 - int(math.floor( (len(real_column))/8 )) )
        value		= "{0}{1}as '{2}'".format( real_column, "\t"*tabs, column_alias )
        column_dict[k]	= value
    return column_dict

class query_set(object):
    def __init__( self, table, alias=None,
                  index=True, joins=True, single=False,
                  structure=None, structure_update=None ):
        self.table		= table
        self.alias		= alias
        self.columns		= get_columns( table, alias )
        self.structure		= structure or get_structure( table )
        if structure_update:
            self.structure.update( structure_update )
        self.joins		= []
        if joins:
            self.joins		= tables.get(table, {}).get('join', [])

        if single == True:
            self.structure['.single']	= True
        if index == False:
            self.structure['.index']	= False

    def join(self, key, path, index=True, single=False):
        table_set		= endpoint(path, joins=False, index=index, single=single)
        table			= table_set.table
        subkey			= self.structure.get(key)

        join			= get_joins( self.table, table )
        self.joins.extend( join )
        self.joins.extend( table_set.joins )
        
        self.columns.update( table_set.columns )
        
        if subkey is False:
            del self.structure[key]
            return

        self.structure[key]	= table_set.structure
        
        if self.structure.get('.key') is None:
            raise Exception("'.key' is required in structure definition")
        
        if type(self.structure['.key']) is list:
            self.structure['.key'].append( key )
        else:
            self.structure['.key']	= [ self.structure['.key'], key ]

    def query(self, crud, where=None, query=None, limit=1000, orderby=None):
        if query is None:
            query = """
    SELECT {columns}
      FROM {table}
           {joins}
     {where}
            """
            if orderby is not None:
                query  += """
           ORDER BY {orderby}
                """.format(orderby=orderby)
            if limit is not None:
                if type(limit) in (str,int,float):
                    limit	= (0, limit)
                query  += """
           LIMIT {0}, {1}
                """.format(*limit)
        columns		= self.columns.values()
        columns.sort()
        query	= query.format(
            columns	= ",\n        ".join( columns ),
            table	= self.table,
            joins	= "\n           ".join( self.joins ),
            where	= where or '',
        )
        log.debug("%s", query)
        cursor		= crud.execute(query)
        return formatter.attach( cursor.fetchall(), self.structure )
