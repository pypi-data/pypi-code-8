# -*- coding: utf-8 -*-

"""
.. module:: prodiguer_client/metrics/formatter/transformer_utils.py
   :copyright: @2015 IPSL (http://ipsl.fr)
   :license: GPL/CeCIL
   :platform: Unix, Windows
   :synopsis: Utility functions used by transformers.

.. moduleauthor:: Insitut Pierre Simon Laplace (IPSL)


"""
from collections import OrderedDict

import arrow



# Date formats used within raw metric outputs.
_DATE_FORMATS = [
    'ddd MMM DD HH:mm:ss YYYY',
    'YYYY-MM-DDTHH:mm:ss'
]


def get_date(value):
    """Returns a date value derived from a string.

    """
    for date_format in _DATE_FORMATS:
        try:
            value = arrow.get(value, date_format)
        except arrow.parser.ParserError:
            pass
        else:
            break

    return unicode(value)


def get_numeric(value):
    """Returns a numeric value derived from a string.

    """
    for numeric_type in (int, float):
        try:
            value = numeric_type(value)
        except ValueError:
            pass
        else:
            break

    return value


def get_value(value):
    """Returns a formatted value derived from a string.

    """
    try:
        value.lower()
    except AttributeError:
        pass
    else:
        if value.lower() in ['n/a', 'nan']:
            return None

    return value


def get_dict(obj):
    """Returns a formatted dictionary.

    """
    keys = sorted(obj.keys())

    return OrderedDict([(k, get_value(obj[k])) for k in keys])
