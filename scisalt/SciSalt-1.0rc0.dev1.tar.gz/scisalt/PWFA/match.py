import numpy as _np
import slactrac as _sltr
from .plasma import *


class Match(object):
    def __init__(self, plasma, E, emit_n):
        self.plasma = plasma
        self.E = E
        self.emit_n = emit_n

    @property
    def gamma(self):
        return _sltr.GeV2gamma(self.E)

    @gamma.setter
    def gamma(self, value):
        self.E = _sltr.gamma2GeV(value)

    @property
    def emit_n(self):
        return self.emit * self.gamma

    @emit_n.setter
    def emit_n(self, value):
        self.emit = value / self.gamma

    @property
    def sigma(self):
        return _np.power(2*_sltr.GeV2joule(self.E)*_sltr.epsilon_0 / (self.plasma.n_p * _np.power(_sltr.e, 2)) , 0.25) * _np.sqrt(self.emit)

    def beta(self, E):
        return 1.0 / _np.sqrt(self.plasma.k_ion(E))
        # return 1.0 / _np.sqrt(2)
