#!/usr/bin/env python

"""
Validate metadata

Copyright 2015, Outernet Inc.
Some rights reserved.

This software is free software licensed under the terms of GPLv3. See COPYING
file that comes with the source code, or http://www.gnu.org/licenses/gpl.txt.
"""

import json

import conz
import validators as v

from . import values

cn = conz.Console()

try:
    FILE_ERRORS = (IOError, OSError, FileNotFoundError)
except NameError:
    FILE_ERRORS = (IOError, OSError,)


VALIDATOR = v.spec_validator(values.SPECS,
                             key=lambda k: lambda obj: obj.get(k))


def load(path):
    """ Load JSON data from file """
    with open(path, 'r') as f:
        data = json.load(f)
    return data


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


def validate_path(path, show_summary=False):
    path = path.strip()
    try:
        data = load(path)
    except FILE_ERRORS:
        cn.pverr(path, 'file not found')
        raise RuntimeError()
    except ValueError:
        cn.pverr(path, 'invalid JSON format')
        raise RuntimeError()
    errors = validate(data)
    if errors:
        err = 'ERR'
        if show_summary:
            err += ' ' + ' '.join(k for k in errors.keys())
        cn.pstd(cn.color.red('{} {}'.format(path, err)))
        for key, err in sorted(errors.items(), key=lambda x: x[0]):
            err, _ = err.args
            cn.pverb('{}: {}'.format(key, cn.color.red(err)))
        return 1
    cn.pstd(cn.color.green('{} OK'.format(path)))
    return 0


def main():
    from .argutil import getparser

    parser = getparser('Validate metadata file',
                       usage='\n    %(prog)s [-h] [-V] PATH\n    '
                       'PATH | %(prog)s [-h] [-V]')
    parser.add_argument('paths', metavar='PATH', help='optional path to '
                        'metadata file (defaults to info.json in current '
                        'directory, ignored if used in a pipe)',
                        default=['./info.json'], nargs='*')
    parser.add_argument('--summary', '-s', action='store_true',
                        help='show a list of invalid keys after ERR')
    args = parser.parse_args()

    if cn.interm:
        cn.verbose = True
        src = args.paths
    else:
        src = cn.readpipe()

    for p in src:
        try:
            validate_path(p, show_summary=args.summary)
        except RuntimeError:
            cn.pstd(cn.color.red('{} ERR'.format(p)))


if __name__ == '__main__':
    main()
