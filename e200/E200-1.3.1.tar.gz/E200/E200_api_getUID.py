import os as _os
on_rtd = _os.environ.get('READTHEDOCS', None) == 'True'
if not on_rtd:
    import numpy as _np
    from scisalt.convertH5ref import convertH5ref as _convertH5ref
from . import classes
# from convertH5ref import convertH5ref as _convertH5ref


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
        vals = _convertH5ref(vals, f)
    except:
        vals = _np.array(vals).flatten()

    return uids[vals == UID]
