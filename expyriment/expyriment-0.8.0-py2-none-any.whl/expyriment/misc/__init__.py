"""The misc package.

This package contains miscellaneous classes, modules and functions.

See also expyriment.misc.extras for more misc.

"""

__author__ = 'Florian Krause <florian@expyriment.org> \
              Oliver Lindemann <oliver@expyriment.org>'
__version__ = '0.8.0'
__revision__ = '19b141b'
__date__ = 'Tue Jun 30 17:14:58 2015 +0200'


import defaults
from _miscellaneous import compare_codes, add_fonts, list_fonts, find_font
from _miscellaneous import unicode2str, str2unicode, numpad_digit_code2ascii
from _miscellaneous import get_monitor_resolution
import constants
from _buffer import  Buffer, ByteBuffer
from _clock import Clock
from _hsv_colour import HSVColour
import geometry
import data_preprocessing
import statistics
