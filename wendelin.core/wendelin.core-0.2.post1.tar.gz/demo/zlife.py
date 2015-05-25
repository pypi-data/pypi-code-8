#!/usr/bin/env python
""" skeleton of using ZBigArray for persistency
    - on first invocation life area is initialized
    - on second and all further invocations, 1 step is made
"""

from wendelin.bigarray.array_zodb import ZBigArray
from ZODB import DB
import transaction
from numpy import uint8


def initialize(life_area):
    # just a 1 point in center
    life_area[:] = 0
    n, m = life_area.shape
    life_area[n//2, m//2] = 1


def iterate(life_area):
    # do some processing of life_area according to game rules
    # XXX for simplicity I just do a right-down cyclic shift
    # life_area - 2D numpy.ndarray
    N = life_area.ravel()
    N[1:] = N[0:-1]


def main():
    dbpath = 'life.fs'
    db = DB(dbpath)
    conn = db.open()
    root = conn.root()

    # initial
    if not root.has_key('life_area'):
        # create ZBigArray and hook it into DB.
        zlife_area = ZBigArray((10,10), uint8)
        root['life_area'] = zlife_area
        root['stepn'] = 0

        # ZBigArray requirement: before we can compute it (with subobject
        # .zfile) have to be made explicitly known to connection or current
        # transaction committed
        transaction.commit()


    zlife_area = root['life_area']  # our ZBigArray
    life_area  = zlife_area[:,:]    # ZBigArray -> ndarray view of it

    # change the data, exactly as if working with numpy.ndarray
    if root['stepn'] == 0:
        initialize(life_area)
    else:
        iterate(life_area)          

    root['stepn'] += 1

    # show life disposition in a pretty way
    print '#step: %i' % root['stepn']
    print life_area

    transaction.commit()
    conn.close()
    db.close()

if __name__ == '__main__':
    main()
