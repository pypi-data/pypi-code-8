"""
Shared values

Copyright 2015, Outernet Inc.
Some rights reserved.

This software is free software licensed under the terms of GPLv3. See COPYING
file that comes with the source code, or http://www.gnu.org/licenses/gpl.txt.
"""

import re

import validators as v


PLACEHOLDER_RE = re.compile(r'^\$[A-Z]+$')
LOCALE_RE = re.compile(r'^[a-z]{2}([_-][a-zA-Z]+)?$', re.I)
COMMASEP_RE = re.compile(r'^[\w ]+(?:, ?[\w ]+)*$', re.U)
RELPATH_RE = re.compile(r'^[^/]+(/[^/]+)*$')
TS_FMT = '%Y-%m-%d %H:%M:%S UTC'
DATE_FMT = '%Y-%m-%d'
LICENSES = ('CC-BY', 'CC-BY-ND', 'CC-BY-NC', 'CC-BY-ND-NC', 'CC-BY-SA',
            'CC-BY-NC-SA', 'GFDL', 'OPL', 'OCL', 'ADL', 'FAL', 'PD', 'OF',
            'ARL', 'ON')
LICENSE_NAMES = (
    'Creative Commons Attribution',
    'Creative Commons Attribution-NoDerivs',
    'Creative Commons Attribution-NonCommercial',
    'Creative Commons Attribution-NonCommercial-NoDerivs',
    'Creative Commons Attribution-ShareAlike',
    'Creative Commons Attribution-NonCommercial-ShareAlike',
    'GNU Free Documentation License',
    'Open Publication License',
    'Open Content License',
    'Against DRM License',
    'Free Art License',
    'Public Domain',
    'Other free license',
    'All rights reserved',
    'Other non-free license',
)
LICENSE_PAIRS = dict(zip(LICENSES, LICENSE_NAMES))

REQUIRED = (
    'title',
    'url',
    'timestamp',
    'broadcast',
    'license',
)

OPTIONAL = (
    'archive',
    'images',
    'index',
    'is_partner',
    'is_sponsored',
    'keep_formatting',
    'keywords',
    'language',
    'multipage',
    'partner',
    'publisher',
)

KEYS = REQUIRED + OPTIONAL

DEFAULTS = {
    'archive': 'core',
    'images': 0,
    'index': 'index.html',
    'is_partner': False,
    'is_sponsored': False,
    'keep_formatting': False,
    'keywords': '',
    'language': '',
    'multipage': False,
    'partner': '',
    'publisher': '',
}

SPECS = {
    'title': [v.required, v.nonempty],
    'url': [v.required, v.nonempty, v.url],
    'timestamp': [v.required, v.nonempty, v.timestamp(TS_FMT)],
    'broadcast': [v.required, v.nonempty,
                  v.OR(v.timestamp(DATE_FMT), v.match(PLACEHOLDER_RE))],
    'license': [v.required, v.isin(LICENSES)],
    'images': [v.optional(), v.istype(int), v.gte(0)],
    'language': [v.optional(''), v.nonempty, v.match(LOCALE_RE)],
    'multipage': [v.optional(), v.istype(bool)],
    'index': [v.optional(''), v.match(RELPATH_RE)],
    'keywords': [v.optional(''), v.nonempty, v.match(COMMASEP_RE)],
    'archive': [v.optional(''), v.nonempty],
    'partner': [v.optional(''), v.nonempty],
    'publisher': [v.optional(''), v.nonempty],
    'is_partner': [v.optional(), v.istype(bool)],
    'is_sponsored': [v.optional(), v.istype(bool)],
    'keep_formatting': [v.optional(), v.istype(bool)],
}
