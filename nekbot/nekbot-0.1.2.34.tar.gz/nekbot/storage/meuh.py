from meuhdb import MeuhDb

__author__ = 'nekmo'

class Meuh(object):
    def __init__(self, plugin, name='global'):
        self.db_name = '%s-%s.json' % (plugin, name)
        self.meuh = MeuhDb(
            path=None,
            autocommit=False, autocommit_after=3,
            lazy_indexes=False)