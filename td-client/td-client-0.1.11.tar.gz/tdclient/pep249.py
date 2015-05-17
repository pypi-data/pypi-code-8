#!/usr/bin/env python

import tdclient

def connect(*args, **kwargs):
    return Connection(*args, **kwargs)

apilevel = "2.0"

threadsafety = 3

paramstyle = "pyformat"

class Warning(Warning):
    pass

class Error(Exception):
    pass

class InterfaceError(Error):
    pass

class DatabaseError(Error):
    pass

class DataError(DatabaseError):
    pass

class OperationalError(DatabaseError):
    pass

class IntegrityError(DatabaseError):
    pass

class InternalError(DatabaseError):
    pass

class ProgrammingError(DatabaseError):
    pass

class NotSupportedError(DatabaseError):
    pass

class Connection(object):
    def __init__(self, database, *args, **kwargs):
        self._client = tdclient.Client(*args, **kwargs)
        self._database = database

    def close(self):
        self._client.close()

    def commit(self):
        raise NotImplementedError

    def rollback(self):
        raise NotImplementedError

    def cursor(self):
        return Cursor(self, self._database)

class Cursor(object):
    def __init__(self, connection, database):
        self._connection = connection
        self._database = database
        self._result = None
        self._description = None
        self._rowcount = None
        self._index = 0

    @property
    def description(self):
        return self._description

    @property
    def rowcount(self):
        return self._rowcount

    def callproc(self, procname, *parameters):
        raise NotImplementedError

    def close(self):
        self._connection.close()

    def execute(self, query, args=None):
        if args is not None:
            if isinstance(args, dict):
                query = query.format(dict)
            else:
                raise NotImplementedError
        job = self._connection._client.query(self._database, query, type="presto")
        job.wait()
        self._result = list(job.result())
        self._rowcount = len(self._result)
        self._description = [ (name, t, None, None, None, None, None) for (name, t) in job._hive_result_schema ]

    def executemany(self, operation, seq_of_parameters):
        for parameter in seq_of_parameters:
            self.execute(operation, *parameter)

    def fetchone(self):
        if self._index < len(self._result):
            row = self._result[self._index]
            self._index += 1
            return row
        else:
            return None

    def fetchmany(size=None):
        if size is None:
            return self.fetchall()
        else:
            rows = []
            for i in range(size):
                row = self._result[self._index]
                self._index += 1
                rows.append(row)
            return rows

    def fetchall(self):
        return list(self._result)

    def nextset(self):
        raise NotImplementedError

    def setinputsizes(self, sizes):
        pass

    def setoutputsize(self, size, column=None):
        pass

Date = None

Time = None

Timestamp = None

def DateFromTicks(ticks):
    pass

def TimeFromTicks(ticks):
    pass

def TimestampFromTicks(ticks):
    pass

def Binary(string):
    pass

STRING = None

BINARY = None

NUMBER = None

DATETIME = None

ROWID = None

