from . import classes                                    # noqa
from . import facettools                                 # noqa
from . import graphics                                   # noqa
from . import hardcode                                   # noqa
# from . import PWFA                                       # noqa

from .BDES2K import *                                    # noqa
from .LinLsqFit import LinLsqFit                         # noqa
from .NonUniformImage import *                           # noqa
from .NonUniformImage_axes import NonUniformImage_axes   # noqa
from .addlabel import addlabel                           # noqa
from .chisquare import chisquare                         # noqa
from .create_group import create_group                   # noqa
from .curve_fit_unscaled import curve_fit_unscaled       # noqa
from .derefdataset import *                              # noqa
from .fft import fft                                     # noqa
from .figure import figure                               # noqa
from .fill_missing_timestamps import *                   # noqa
from .findpinch import findpinch                         # noqa
from .fitimageslice import fitimageslice                 # noqa
from .frexp10 import *                                   # noqa
from .gaussfit import _gauss                             # noqa
from .gaussfit import _gaussvar                          # noqa
from .gaussfit import gaussfit                           # noqa
from .h5drill import *                                   # noqa
from .hist import hist                                   # noqa
from .hist2d import hist2d                               # noqa
from .imshow_slider import imshow_slider                 # noqa
from .imshow_batch import imshow_batch                   # noqa
from .linspaceborders import linspaceborders             # noqa
from .linspacestep import linspacestep                   # noqa
from .mylogger import *                                  # noqa
from .pcolor_axes import pcolor_axes                     # noqa
from .picklejar import picklejar                         # noqa
from .plot_featured import plot_featured                 # noqa
from .rgb2gray import rgb2gray                           # noqa
from .showfig import showfig                             # noqa
from .setup_figure import setup_figure                   # noqa


class Error(Exception):
    """Base class for exceptions in this module."""
    pass


class ArgumentError(Error):
    """Exception raised for errors in function arguments.

    Attributes:
        arg -- input argument in which the error occurred
        msg -- explanation of the error
    """

    def __init__(self, arg, msg):
        self.arg = arg
        self.msg = msg
