import collections
from bq.util.paths import bisque_path
from bq.release import __VERSION_HASH__

def file_root():
    return bisque_path('')
def file_public():
    return bisque_path('public')



BQTemplateGlobal = collections.namedtuple ('BQTemplateGlobal', ['url', 'config'] )

def bqurl (url, params=None):
    return url

def make_bq (request):
    bqglobal = BQTemplateGlobal ( url = bqurl, config = request.registry.settings)
    return bqglobal
