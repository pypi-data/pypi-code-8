"""
Backwards compatibility for Python 2
"""


import sys


if sys.version_info[0] is 2:  # pragma no cover
    string_types = (str, unicode)
else:  # pragma no cover
    string_types = str,
