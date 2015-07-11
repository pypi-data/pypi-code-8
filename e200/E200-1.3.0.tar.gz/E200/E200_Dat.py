import inspect as _ins
import os
on_rtd = os.environ.get('READTHEDOCS', None) == 'True'
if on_rtd:
    import re as _np
else:
    import numpy as _np


__all__ = ['E200_Dat']


class E200_Dat(object):
    """
    Contains data. This is designed to prevent accidental incorrect correlation of data with UIDs, in case a request for data cannot find UIDs.

    **Should not be created directly, only accessed through** :func:`E200.E200_load_images`\ **.**
    """
    def __dir__(self):
        return [val[0] for val in _ins.getmembers(self)]

    def __init__(self, dat, uid, field):
        self._dat = _np.array([dat]).flatten()
        self._uid = _np.int64([uid]).flatten()
        self._field = field

    def __len__(self):
        return len(self._uid)

    @property
    def dat(self):
        """
        An array of data correlated to :attr:`E200.E200_Dat.UID`.
        """
        return self._dat

    def _get_uid(self):
        """
        An array of UIDs correlated to :attr:`E200.E200_Dat.dat`.
        """
        return self._uid
    uid = property(_get_uid)
    UID = property(_get_uid)

    @property
    def field(self):
        """
        Field data was loaded from.
        """
        return self._field
