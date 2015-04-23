"""
jasco_parser

a text parser which parse JASCO (www.jasco.co.jp) style text and return XY or
XYZ numeric data
"""
__author__ = 'Alisue <lambdalisue@hashnote.net>'
__all__ = ('__version__', 'VERSION', 'parse', 'load')
from app_version import get_versions
from jasco_parser.parser import JASCOParser

__version__, VERSION = get_versions('jasco_parser')


def parse(iterable, delimiter=None):
    """
    Parse JASCO style text and return XY or XYZ numerical data

    Args:
        iterable: An iterable object
        delimiter: A delimiter. Default is None

    Returns:
        A list
    """
    return JASCOParser().parse(iterable, delimiter)


def load(filename, delimiter=None):
    """
    Load JASCO style text and return XY or XYZ numerical data

    Args:
        filename: A filename
        delimiter: A delimiter. Default is None

    Returns:
        A list
    """
    return JASCOParser().load(filename, delimiter)
