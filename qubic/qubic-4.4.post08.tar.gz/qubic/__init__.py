from . import calfiles
from . import data
from . import io
from .acquisition import *
from .beams import *
from .calibration import *
from .cl import *
from .instrument import *
from .mapmaking import *
from .samplings import *
from .scene import *
from .xpol import *


def full(shape, fill_value, dtype=None, order='C'):
    import numpy as np
    out = np.empty(shape, dtype=dtype, order=order)
    out[...] = fill_value
    return out


def full_like(a, fill_value, dtype=None, order='K', subok=True):
    import numpy as np
    out = np.empty_like(a, dtype=dtype, order=order, subok=subok)
    out[...] = fill_value
    return out

import numpy
if numpy.__version__ < '1.8':
    numpy.full = full
    numpy.full_like = full_like
del full, full_like, numpy

__version__ = '4.4.post08'
