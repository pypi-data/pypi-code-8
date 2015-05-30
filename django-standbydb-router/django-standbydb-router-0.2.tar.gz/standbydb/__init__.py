"""
With :class:`standbydb.MasterStandbyRouter` all read queries will go to a standby
database;  all inserts, updates, and deletes will do to the ``default``
database.

First, define ``STANDBY_DATABASES`` in your settings.  It should be a list of
database aliases that can be found in ``DATABASES``::

    DATABASES = {
        'default': {...},
        'standby-1': {...},
        'standby-2': {...},
    }
    STANDBY_DATABASES = ['standby-1', 'standby-2']

Then put ``standbydb.MasterStandbyRouter`` into DATABASE_ROUTERS::

    DATABASE_ROUTERS = ('standbydb.MasterStandbyRouter',)

The standby databases will be chosen in round-robin fashion.

If you want to get a connection to a standby in your app, use
:func:`standbydb.get_standby`::

    from django.db import connections
    import standbydb

    connection = connections[standbydb.get_standby()]
"""
import itertools
import random
from distutils.version import LooseVersion

import django
from django.conf import settings


DEFAULT_DB_ALIAS = 'default'


if getattr(settings, 'STANDBY_DATABASES'):
    # Shuffle the list so the first standby db isn't slammed during startup.
    dbs = list(settings.STANDBY_DATABASES)
    random.shuffle(dbs)
    standbys = itertools.cycle(dbs)
    # Set the standbys as test mirrors of the master.
    for db in dbs:
        if LooseVersion(django.get_version()) >= LooseVersion('1.7'):
            settings.DATABASES[db].get('TEST', {})['MIRROR'] = DEFAULT_DB_ALIAS
        else:
            settings.DATABASES[db]['TEST_MIRROR'] = DEFAULT_DB_ALIAS
else:
    standbys = itertools.repeat(DEFAULT_DB_ALIAS)


def get_standby():
    """Returns the alias of a standby database."""
    return next(standbys)


class MasterStandbyRouter(object):
    """Router that sends all reads to a standby, all writes to default."""

    def db_for_read(self, model, **hints):
        """Send reads to standbys in round-robin."""
        return get_standby()

    def db_for_write(self, model, **hints):
        """Send all writes to the master."""
        return DEFAULT_DB_ALIAS

    def allow_relation(self, obj1, obj2, **hints):
        """Allow all relations, so FK validation stays quiet."""
        return True

    def allow_syncdb(self, db, model):
        """Only allow syncdb on the master."""
        return db == DEFAULT_DB_ALIAS

