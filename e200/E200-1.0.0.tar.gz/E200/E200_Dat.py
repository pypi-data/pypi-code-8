import numpy as _np

__all__ = ['E200_Dat']


class E200_Dat(object):
    def __init__(self, dat, uid, field):
        self._dat = _np.array([dat]).flatten()
        self._uid = _np.int64([uid]).flatten()
        self._field = field

    def __len__(self):
        return len(self._uid)

    def _get_dat(self):
        return self._dat
    dat = property(_get_dat)

    def _get_uid(self):
        return self._uid
    uid = property(_get_uid)
    UID = property(_get_uid)

    def _get_field(self):
        return self._field
    field = property(_get_field)
