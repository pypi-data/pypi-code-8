import os
from nekbot import settings

__author__ = 'nekmo'

import pyejdb

def ejdb(plugin, collection='global'):
    name = 'ejdb-%s' % collection
    path = os.path.join(settings.STORAGE_DIR, plugin, name)
    try:
        os.makedirs(os.path.dirname(path))
    except:
        pass
    return pyejdb.EJDB(path)