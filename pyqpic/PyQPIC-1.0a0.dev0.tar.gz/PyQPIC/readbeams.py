import h5py as _h5
import os as _os
import scisalt as _mt


class Beam(object):
    def __init__(self, nbeam=1, tstep=0, path=None):
        if path is None:
            path = _os.getcwd()

        self._nbeam = nbeam
        self._tstep = tstep

        rel_filepath = 'RAW-BEAM/{nbeam:02.0f}/RAW-BEAM-{nbeam:02.0f}_{tstep:04.0f}.h5'.format(nbeam=nbeam, tstep=tstep)
        self._filepath = _os.path.join(path, rel_filepath)

        self._h5file = _h5.File(self.filepath, 'r')
        self._h5 = _mt.H5Drill(self._h5file)

    @property
    def filepath(self):
        return self._filepath

    @property
    def x(self):
        try:
            return self._x
        except AttributeError:
            self._x = self._h5.x1.value
            return self._x

    @property
    def xp(self):
        try:
            return self._xp
        except AttributeError:
            self._xp = self._h5.p1.value
            return self._xp

    @property
    def y(self):
        try:
            return self._y
        except AttributeError:
            self._y = self._h5.x2.value
            return self._y

    @property
    def yp(self):
        try:
            return self._yp
        except AttributeError:
            self._yp = self._h5.p2.value
            return self._yp
        
    @property
    def z(self):
        try:
            return self._z
        except AttributeError:
            self._z = self._h5.x3.value
            return self._z

    @property
    def gamma(self):
        try:
            return self._gamma
        except AttributeError:
            self._gamma = self._h5.p3.value
            return self._gamma
