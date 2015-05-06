import logging
import numpy as np
from matmodlab.utils.errors import StopFortran

xpansion = None

class Expansion(object):
    def __init__(self, exp_type, data):
        data = np.array(data)
        self._type = exp_type.upper()
        if self._type == "ISOTROPIC":
            if len(data) != 1:
                raise ValueError("unexpected value for isotropic expansion")
        else:
            raise ValueError("{0}: unknown expansion type".format(exp_type))
        self._data = data

    def setup(self):
        global xpansion
        try:
            from lib.expansion import expansion as xpansion
        except ImportError:
            raise ImportError('lib.expansion.so not imported')

    def update_state(self, temp, dtemp, F, kappa):
        log = logging.getLogger('mps')
        Fm, Em = xpansion.mechdef(self.data, temp, dtemp, kappa, F,
                                  log.info, log.warn, StopFortran)
        return Fm, Em

    @property
    def data(self):
        return self._data
