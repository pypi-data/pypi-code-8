import os
import json

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

def getTI0(mypath):
    onlyfiles = [os.path.join(mypath,f) for f in os.listdir(mypath) if
                 os.path.isfile(os.path.join(mypath,f)) and f.endswith('json')]
    ti = None; dt= None
    for f in onlyfiles:
        dt = f.split(os.sep)[-1].split('.')[0]
        if f.endswith('vola.json'):
            pass
        else:
            j = json.load(open(f))
            ti = j['_tinfo']
    return ti, dt


def getTI(sym):
    from config import TRADEINFODIR
    mypath = TRADEINFODIR + os.sep + sym
    return getTI0(mypath)


if __name__ == "__main__":
    from pprint import pprint
    ti, dt = getTI('YY')
    pprint(ti)