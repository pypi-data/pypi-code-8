import os as _os
on_rtd = _os.environ.get('READTHEDOCS', None) == 'True'
if not on_rtd:
    import numpy as _np
from . import classes


def E200_api_getUID(dataset, val, f=None):
    """
    Return all UIDs where *val* is equal to the value of the ``dat`` member of *dataset* (which must be either an :class:`E200.Drill` or an :class:`h5py.Group` class).

    Returns an ``array`` of UIDs.
    """
    if type(dataset) == classes.Drill:
        dataset = dataset._hdf5
        
    if f is None:
        f = dataset.file
    uids = dataset['UID']
    vals = dataset['dat']

    uids = uids[:, 0]
    try:
        vals = convertH5ref(vals, f)
    except:
        vals = _np.array(vals).flatten()

    return uids[vals == val]

def convertH5ref(dataset, f):
    """
    Dereferences *dataset* of type :mod:`h5py._hl.files.File` using file *f*
    """
    vals = _np.array([])
    for ref in dataset[:, 0]:
        vals = _np.append(vals, f[ref])

    return vals
