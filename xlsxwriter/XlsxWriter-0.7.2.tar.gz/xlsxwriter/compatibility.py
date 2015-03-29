###############################################################################
#
# Python 2/3 compatibility functions for XlsxWriter.
#
# Copyright (c), 2013-2015, John McNamara, jmcnamara@cpan.org
#

import sys
from decimal import Decimal

try:
    # For compatibility between Python 2 and 3.
    from StringIO import StringIO
except ImportError:
    from io import StringIO

try:
    # For Python 2.6+.
    from fractions import Fraction
except ImportError:
    Fraction = float

try:
    # For Python 2.6+.
    from collections import defaultdict
    from collections import namedtuple
except ImportError:
    # For Python 2.5 support.
    from .compat_collections import defaultdict
    from .compat_collections import namedtuple

# Types to check in Python 2/3.
if sys.version_info[0] == 2:
    num_types = (float, int, long, Decimal, Fraction)
    str_types = basestring
else:
    num_types = (float, int, Decimal, Fraction)
    str_types = str


if sys.version_info < (2, 6, 0):
    from StringIO import StringIO as BytesIO
else:
    from io import BytesIO as BytesIO
