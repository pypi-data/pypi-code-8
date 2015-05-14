"""
Validator to use a library

Copyright 2015, Outernet Inc.
Some rights reserved.

This software is free software licensed under the terms of GPLv3. See COPYING
file that comes with the source code, or http://www.gnu.org/licenses/gpl.txt.
"""

import validators

from . import values


VALIDATOR = validators.spec_validator(
    values.SPECS, key=lambda k: lambda obj: obj.get(k))


def validate(data):
    res = VALIDATOR(data)
    if res:
        return res
    # Additional validation that cannot be done using the specs
    if 'publisher' not in data or 'partner' not in data:
        return {}
    if data['publisher'] == data['partner']:
        return {}
    return {
        'publisher': ValueError('must match partner'),
        'partner': ValueError('must match publisher')
    }
