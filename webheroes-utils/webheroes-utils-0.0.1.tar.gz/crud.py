
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

__all__				= ["connect", "reconnect", "reset_transaction",
                                   "execute", "read", "create", "update",
                                   "delete", "end_transaction"]

from .			import logging

import MySQLdb		as mysqldb
import MySQLdb.cursors	as mysql_cursors

import time
timer			= time.time

log			= logging.getLogger('crud')
log.setLevel(logging.DEBUG)
last_query		= None
last_args		= None
connection_args		= None
db, cursor		= None, None

def connect(*args, **kwargs):
    global db, cursor, connection_args
    if "cursorclass" not in kwargs:
        kwargs['cursorclass']	= mysql_cursors.DictCursor
    elif kwargs['cursorclass'] in [None, False]:
        del kwargs['cursorclass']
    connection_args	= (args, kwargs)
    db			= mysqldb.connect(*args, **kwargs )
    cursor		= db.cursor()

def reconnect():
    global db, cursor, connection_args
    if connection_args is not None:
        args, kwargs	= connection_args
    db			= mysqldb.connect(*args, **kwargs)
    cursor		= db.cursor()

def reset_transaction():
    global db
    try:
        db.commit()
    except (AttributeError, mysqldb.OperationalError) as e:
        log.error("%s: reconnecting to mysql server", e)
        reconnect()
    
def execute(query, args=None):
    global db, cursor, last_query, last_args
    reset_transaction()
    last_query		= query
    last_args		= args
    log.debug("QUERY: %s\n%s", query, args)
    start		= timer()
    cursor.execute(query, args)
    log.debug("QUERY TIME: %s", timer() - start)
    return cursor

def read(query, args=None):
    return execute(query, args)

def create(table, columns, values, commit=True, test=False):
    global db, cursor
    log.debug("data given: (%s) %s", columns, values)
    cols		= "`,`".join(columns)
    args		= tuple(values)
    vals		= ", ".join(["%s" for i in range(len(args))])
    query		= """
    INSERT INTO `{table}` (`{cols}`)
    VALUES ({vals})
    """.format(table=table, cols=cols, vals=vals)
    
    log.debug("QUERY: %s", query)
    execute(query, args)

    if commit:
        end_transaction(test)
    return cursor.lastrowid

def update(table, data, where, commit=True, test=False):
    global db, cursor
    sets		= ", ".join(["`%s`=%%s" % (k,) for k,v in data.items()])
    args		= tuple(data.values()+[where[1]])
    where		= where[0]
    query		= """
    UPDATE `{table}`
       SET {sets}
     WHERE {where}
    """.format(table=table, sets=sets, where=where)
    
    log.debug("QUERY: %s", query)
    execute(query, args)
    
    if commit:
        end_transaction(test)
    return cursor.rowcount

def delete(table, where, commit=True, test=False):
    global db, cursor
    args		= (where[1],)
    query		= """
    DELETE FROM `{table}`
     WHERE {where}
    """.format(table=table, where=where[0])
    
    log.debug("QUERY: %s", query)
    execute(query, args)
    
    if commit:
        end_transaction(test)
    return cursor.rowcount

def end_transaction(test=False):
    global db, cursor
    if test:
        log.warn("Rollback changes")
        db.rollback()
    else:
        db.commit()
