import numpy as _np
import slactrac as _sltr


class Plasma(object):
    def __init__(self, n_p=None, n_p_cgs=None):
        if n_p is None and n_p_cgs is None:
            raise ValueError('Keywords n_p and n_p_cgs cannot both be None')
        elif n_p is not None and n_p_cgs is not None:
            raise ValueError('Keywords n_p and n_p_cgs cannot both be specified')
        elif n_p is not None:
            self.n_p = n_p
        elif n_p_cgs is not None:
            self.n_p_cgs = n_p_cgs

    # @property
    # def n_p(self):
    #     return self._n_p

    # @n_p.setter
    # def n_p(self, n_p):
    #     self._n_p = n_p

    @property
    def w_p(self):
        return _np.sqrt(self.n_p * _np.power(_sltr.e, 2) / (_sltr.m_e * _sltr.epsilon_0))

    def k_ion(self, E):
        return self.n_p * _np.power(_sltr.e, 2) / (2*_sltr.GeV2joule(E) * _sltr.epsilon_0)

    @property
    def n_p_cgs(self):
        return self.n_p / 1e6

    @n_p_cgs.setter
    def n_p_cgs(self, n_p_cgs):
        self.n_p = n_p_cgs * 1e6
