#!/usr/bin/env python
# -*- coding: utf-8 -*-

'''
Simple Psycopg2 Wrapper

:copyright: (c) 2015 Gary Chambers
:license: MIT
'''

from __future__ import print_function, unicode_literals, division
from psycopg2 import (IntegrityError, InterfaceError, DatabaseError,
                      ProgrammingError)
from .psypg_wrap import PgConfig, pg_query, pg_commit, pg_rollback

__title__ = 'psypg'
__version__ = '1.1'
__all__ = ['IntegrityError', 'InterfaceError', 'DatabaseError',
           'ProgrammingError', 'PgConfig', 'pg_query']
