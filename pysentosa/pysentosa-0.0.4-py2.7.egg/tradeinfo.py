__author__ = 'Wu Fuheng'
import config
import os
from os import listdir
from os.path import isfile, join
import json
from pprint import pprint
from utils import getLastPrice

POSITION_STATUS = [
  'NOPOSITION',
  'OPENTRADE_LONG',
  'OPENTRADE_SHORT',
  'DELIMITERSTATUS',
  'WAITCLOSEFILL_L',
  'WAITCLOSEFILL_S',
  'WAITLONGFILL',
  'WAITSHORFILL'
]

account = config.yml_sentosa['global']['account']
fpath = config.yml_sentosa['linux']['TRADEINFODIR'] + os.sep + account

def getTI(sym):
    mypath = fpath + '/' + sym
    onlyfiles = [join(mypath,f) for f in listdir(mypath) if isfile(join(mypath,f)) and f.endswith('json')]
    print getLastPrice(sym)
    for f in onlyfiles:
        dt = f.split(os.sep)[-1].split('.')[0]
        if f.endswith('vola.json'):
            pass
        else:
            j = json.load(open(f))
            ti = j['_tinfo']
            print ti['__ps'][0] * ti['__vo'][0]
            #print POSITION_STATUS[ti['__status']]
    return ti, dt

ti, dt = getTI('YY')
pprint(ti)