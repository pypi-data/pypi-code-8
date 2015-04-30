# -*- encoding: utf-8 -*-
# json_delta: a library for computing deltas between JSON-serializable
# structures.
# json_delta/_util.py
#
# Copyright 2012‒2015 Philip J. Roberts <himself@phil-roberts.name>.
# BSD License applies; see the LICENSE file, or
# http://opensource.org/licenses/BSD-2-Clause
'''
Utility functions and constants used by all submodules.
'''
from __future__ import print_function, unicode_literals

import json

try:
    Basestring = basestring
except NameError:
    Basestring = str

TERMINALS = (str, int, float, bool, type(None))
try:
    TERMINALS += (unicode, long)
except NameError:
    pass
NONTERMINALS = (list, dict)
SERIALIZABLE_TYPES = TERMINALS + NONTERMINALS

# ----------------------------------------------------------------------
# Utility functions

def uniquify(obj, key=lambda x: x):
    '''Remove duplicate elements from a list while preserving order.'''
    seen = set()
    seen_add = seen.add
    return [x for x in obj if
            (key(x) not in seen and
             not seen_add(key(x)))]

def decode_json(file_or_str):
    '''Decode a JSON file-like object or string.

    The following doctest is probably pointless as documentation.  It is
    here so json_delta can claim 100% code coverage for its test suite!

    >>> try:
    ...     from StringIO import StringIO
    ... except ImportError:
    ...     from io import StringIO
    >>> foo = '[]'
    >>> decode_json(foo)
    []
    >>> decode_json(StringIO(foo))
    []
    '''
    if isinstance(file_or_str, Basestring):
        return json.loads(file_or_str)
    else:
        return json.load(file_or_str)

def _load_and_func(func, parm1=None, parm2=None, both=None, **flags):
    '''Decode JSON-serialized parameters and apply func to them.'''
    if (parm1 is not None) and (parm2 is not None):
        return func(decode_json(parm1), decode_json(parm2), **flags)
    else:
        assert (both is not None), (parm1, parm2, both)
        [parm1, parm2] = decode_json(both)
        return func(parm1, parm2, **flags)

def in_one_level(diff, key):
    '''Return the subset of ``diff`` whose key-paths begin with
    ``key``, expressed relative to the structure at ``[key]``
    (i.e. with the first element of each key-path stripped off).

    >>> diff = [ [['bar'], None],
    ...          [['baz', 3], 'cheese'],
    ...          [['baz', 4, 'quux'], 'foo'] ]
    >>> in_one_level(diff, 'baz') == [[[3], 'cheese'], [[4, 'quux'], 'foo']]
    True
    '''
    oper_stanzas = [stanza[:] for stanza in diff if stanza[0][0] == key]
    for stanza in oper_stanzas:
        stanza[0] = stanza[0][1:]
    return oper_stanzas

def compact_json_dumps(obj):
    '''Compute the most compact possible JSON representation of the
    serializable object ``obj``.

    >>> test = {
    ...             'foo': 'bar',
    ...             'baz':
    ...                ['quux', 'spam',
    ...       'eggs']
    ... }
    >>> compact_json_dumps(test) in (
    ...     '{"foo":"bar","baz":["quux","spam","eggs"]}',
    ...     '{"baz":["quux","spam","eggs"],"foo":"bar"}'
    ... )
    True
    >>>
    '''
    return json.dumps(obj, indent=None, separators=(',', ':'))

def all_paths(struc):
    '''Generate key-paths to every node in ``struc``.

    Both terminal and non-terminal nodes are visited, like so:

    >>> paths = [x for x in all_paths({'foo': None, 'bar': ['baz', 'quux']})]
    >>> [] in paths # ([] is the path to struc itself.)
    True
    >>> ['foo'] in paths
    True
    >>> ['bar'] in paths
    True
    >>> ['bar', 0] in paths
    True
    >>> ['bar', 1] in paths
    True
    >>> len(paths)
    5
    '''
    yield []
    if isinstance(struc, dict):
        keys = struc.keys()
    elif isinstance(struc, list):
        keys = range(len(struc))
    else:
        return
    for key in keys:
        for subkey in all_paths(struc[key]):
            yield [key] + subkey

def follow_path(struc, path):
    '''Return the value found at the key-path ``path`` within ``struc``.'''
    if not path:
        return struc
    else:
        return follow_path(struc[path[0]], path[1:])

def check_diff_structure(diff):
    '''Return ``diff`` (or ``True``) if it is structured as a sequence
    of ``diff`` stanzas.  Otherwise return ``False``.

    ``[]`` is a valid diff, so if it is passed to this function, the
    return value is ``True``, so that the return value is always true
    in a Boolean context if ``diff`` is valid.

    >>> check_diff_structure('This is certainly not a diff!')
    False
    >>> check_diff_structure([])
    True
    >>> check_diff_structure([None])
    False
    >>> example_valid_diff = [[["foo", 6, 12815316313, "bar"], None]]
    >>> check_diff_structure(example_valid_diff) == example_valid_diff
    True
    >>> check_diff_structure([[["foo", 6, 12815316313, "bar"], None],
    ...                       [["foo", False], True]])
    False
    '''
    if diff == []:
        return True
    if not isinstance(diff, list):
        return False
    for stanza in diff:
        conditions = (lambda s: isinstance(s, list),
                      lambda s: isinstance(s[0], list),
                      lambda s: len(s) in (1, 2))
        for condition in conditions:
            if not condition(stanza):
                return False
        for key in stanza[0]:
            if not (type(key) is int or isinstance(key, Basestring)):
                # So, it turns out isinstance(False, int)
                # evaluates to True!
                return False
    return diff
