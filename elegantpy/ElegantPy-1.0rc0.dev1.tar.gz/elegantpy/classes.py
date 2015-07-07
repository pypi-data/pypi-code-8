from sdds import SDDS
import numpy as _np
import ipdb
import os

__all__ = ['Final', 'Bunch', 'Matrix', 'ElegantSim']


# ======================================
# Creates a property and removes
# corresponding key from dict
# ======================================
def property_from_dict(name, simple_docstr=None, datfield='_SDDS_param'):
    if simple_docstr is None:
        docstr = '{} in final output file'.format(name)
    else:
        docstr = '{} in final output file'.format(simple_docstr)

    def _get_value(self):
        private_name = '_{}'.format(name)

        try:
            val = getattr(self, private_name)
        except:
            dct = getattr(self, datfield)
            val = dct.pop(name)[0]
            setattr(self, private_name, val)

        if type(val) is int:
            out = _np.int(val)
        elif type(val) == float:
            out = _np.float(val)
        elif type(val) == list:
            out = _np.array(val)
        else:
            raise NotImplementedError('This data type isn''t handled.')

        return out
    return property(_get_value, doc=docstr)


# ======================================
# Defines a meta class for SDDS files
# that creates properties dynamically
# ======================================
class SDDSMeta(type):
    def __new__(cls, name, parents, dct):
        #  ipdb.set_trace()
        if name == 'Final':
            param_properties = [['Charge', None],
                    ['Particles', 'Number of particles'],
                    ['pAverage', 'Average momentum of particles'],
                    ['pCentral', 'Design momentum of beamline']
                ]
        elif name == 'Bunch':
            param_properties = [
                ['Particles', 'Number of particles'],
                ['pCentral', 'Average momentum of bunch (?)']
                ]
            col_properties = [
                ['x', 'x coordinate'],
                ['xp', 'xp coordinate'],
                ['y', 'y coordinate'],
                ['yp', 'yp coordinate'],
                ['t', 't coordinate'],
                ['p', 'p coordinate'],
                ['particleID', 'Particle ID number']
                ]

        try:
            for val in param_properties:
                propname = val[0]
                simple_docstr = val[1]
                dct[propname] = property_from_dict(name=propname, simple_docstr=simple_docstr)
        except:
            pass

        try:
            for val in col_properties:
                propname = val[0]
                simple_docstr = val[1]
                dct[propname] = property_from_dict(name=propname, simple_docstr=simple_docstr, datfield='_SDDS_col')
        except:
            pass

        return super(SDDSMeta, cls).__new__(cls, name, parents, dct)


class SDDSIntermediate(object):
    __metaclass__ = SDDSMeta

    def __init__(self, filename):
        self._SDDS = SDDS(0)
        if os.path.exists(filename):
            self._SDDS.load(filename)
        else:
            raise IOError('File not found: {}'.format(filename))

    @property
    def _SDDS_param(self):
        try:
            return self._SDDS_param_dat
        except:
            self._SDDS_param_dat = dict(zip(self._SDDS.parameterName, self._SDDS.parameterData))
            return self._SDDS_param_dat

    @property
    def _SDDS_col(self):
        try:
            return self._SDDS_column_dat
        except:
            self._SDDS_column_dat = dict(zip(self._SDDS.columnName, self._SDDS.columnData))
            return self._SDDS_column_dat


# ======================================
# Defines a class that represents the
# final output of a simulation
# ======================================
class Final(SDDSIntermediate):
    #  __metaclass__ = SDDSMeta

    @property
    def R(self):
        """Get the R matrix from the final output file"""
        try:
            return self._R
        except:
            # ======================================
            # Get the R matrix from the file
            # ======================================
            self._R = _np.zeros((6, 6))
            for i in range(0, 6):
                istr = '{}'.format(i+1)
                for j in range(0, 6):
                    jstr = '{}'.format(j+1)
                    Rstr = 'R{}{}'.format(istr, jstr)
                    self._R[i, j] = _np.float64(self._SDDS_param.pop(Rstr)[0])
        return self._R

    @property
    def sigma(self):
        """Get the sigma matrix from the final output file"""
        try:
            return self._sigma
        except:
            self._sigma = _np.zeros((6, 6))
            for i in range(0, 6):
                istr = '{}'.format(i+1)
                for j in range(i+1, 6):
                    jstr = '{}'.format(j+1)
                    sstr = 's{}{}'.format(istr, jstr)
                    self._sigma[i, j] = _np.float64(self._SDDS_param.pop(sstr)[0])
                    self._sigma[j, i] = self._sigma[i, j]
            return self._sigma


class Bunch(SDDSIntermediate):
    @property
    def delta(self):
        """Get the delta coordinates"""
        try:
            return self._delta
        except:
            pavg = _np.mean(self.p)
            self._delta = (self.p/pavg-_np.float_(1))
            return self._delta


class Matrix(SDDSIntermediate):
    @property
    def T(self):
        """Get the delta coordinates"""
        try:
            return self._T
        except:
            # ======================================
            # Get the R matrix from the file
            # ======================================
            self._T = _np.zeros((6, 6, 6))
            for i in range(0, 6):
                istr = '{}'.format(i+1)
                for j in range(0, i+1):
                    jstr = '{}'.format(j+1)
                    for k in range(0, j+1):
                        kstr = '{}'.format(k+1)
                        Tstr = 'T{}{}{}'.format(istr, jstr, kstr)
                        self._T[i, j, k] = _np.float64(self._SDDS_col.pop(Tstr))[0, -1]
                        self._T[i, k, j] = self._T[i, j, k]
        return self._T


class ElegantSim(object):
    def __init__(self, path):
        # Get absolute path
        fullpath = os.path.abspath(path)

        # Get root, ext, fulldir
        filename = os.path.basename(fullpath)
        root, ext = os.path.splitext(filename)
        fulldir  = os.path.dirname(fullpath)

        # Get filenames of files to load
        final_file = os.path.join(fulldir, '{}.fin'.format(root))
        bunch_file = os.path.join(fulldir, '{}.out'.format(root))
        mat_file   = os.path.join(fulldir, '{}.mat'.format(root))

        # Load files
        self.Bunch = Bunch(bunch_file)
        self.Matrix = Matrix(mat_file)
        self.Final = Final(final_file)
