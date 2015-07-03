import numpy as _np
from . import classes
# from convertH5ref import convertH5ref as _convertH5ref
from scisalt.convertH5ref import convertH5ref as _convertH5ref


def E200_api_getUID(struct, val, f=None):
    if type(struct) == classes.Drill:
        struct = struct._hdf5
        
    if f is None:
        f = struct.file
    uids = struct['UID']
    vals = struct['dat']

    uids = uids[:, 0]
    try:
        vals = _convertH5ref(vals, f)
    except:
        vals = _np.array(vals).flatten()

    return uids[vals == val]
