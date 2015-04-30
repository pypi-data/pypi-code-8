# -*- encoding: utf-8 -*-
# json_delta: a library for computing deltas between JSON-serializable
# structures.
# json_delta/_upatch.py
#
# Copyright 2012‒2015 Philip J. Roberts <himself@phil-roberts.name>.
# BSD License applies; see the LICENSE file, or
# http://opensource.org/licenses/BSD-2-Clause
'''
Functions for applying udiffs as patches.
'''
from ._util import all_paths, follow_path
from ._patch import patch
from ._diff import compute_keysets

import re
import copy
from json import decoder, scanner

def upatch(struc, udiff, reverse=False, in_place=True):
    '''Apply a patch of the form output by udiff() to the structure
    ``struc``.

    By default, this function modifies ``struc`` in place; set
    ``in_place`` to ``False`` to return a patched copy of ``struc``
    instead.
    '''
    if not in_place:
        struc = copy.deepcopy(struc)
    left_json, right_json = split_udiff_parts(udiff)
    if not (left_json or right_json):
        return struc
    dec = extended_json_decoder()
    left_part = dec.decode(left_json)
    right_part = dec.decode(right_json)
    if reverse:
        return fill_in_ellipses(struc, right_part, left_part)
    return fill_in_ellipses(struc, left_part, right_part)

def extended_json_decoder():
    '''Return a decoder for the superset of JSON understood by the
    upatch function.

    The exact nature of this superset is documented in the manpage for
    json_patch(1).  Briefly, the string ``...`` is accepted where
    standard JSON expects a ``{<property name>}: {<object>}``
    construction, and the string ``...``, optionally followed by a
    number in parentheses, is accepted where standard JSON expects an
    array element.

    The superset is implemented by parsing ``...`` in JSON objects as
    a key/value pair ``Ellipsis: True`` in the resulting dictionary,
    and ``...({num}){?}`` as a subsequence of ``{num}`` ``Ellipsis``
    objects, or one ellipsis object if ``({num})`` is not present.

    Examples:

    >>> dec = extended_json_decoder()
    >>> (dec.decode('{"foo": "bar",...,"baz": "quux"}') ==
    ...  {"foo": "bar", "baz": "quux", Ellipsis: True})
    True
    >>> dec.decode('[...]')
    [Ellipsis]
    >>> (dec.decode('["foo",...(3),"bar"]') ==
    ...  ['foo', Ellipsis, Ellipsis, Ellipsis, 'bar'])
    True
    '''
    dec = decoder.JSONDecoder()
    dec.parse_object = _JSONObject
    dec.parse_array = _JSONArray
    dec.scan_once = scanner.py_make_scanner(dec)
    return dec

# The following functions are taken from the internals of the json
# module, and extended to cope with the udiff superset.

def _JSONObject(s_and_end, *args):
    # The function signature of json.scanner.JSONObject() changed
    # between python versions 2.7 and 3.  The following is an ugly
    # shim to compensate.
    _w = decoder.WHITESPACE.match
    _ws = decoder.WHITESPACE_STR
    if isinstance(args[0], bool):
        (strict, scan_once, object_hook, object_pairs_hook, memo) = args
    else:
        (encoding, strict, scan_once, object_hook, object_pairs_hook) = args

    def check_ellipsis(end):
        'Increments end appropriately if the next three characters are "...".'
        if s[end:end+3] == '...':
            pairs_append((Ellipsis, True))
            end += 3
            if s[end] == ',':
                end += 1
        return end
    def consume_whitespace(end):
        'Increments end to skip any whitespace.'
        try:
            nextchar = s[end]
            if nextchar in _ws:
                end += 1
                nextchar = s[end]
                if nextchar in _ws:
                    end = _w(s, end + 1).end()
                    nextchar = s[end]
        except IndexError:
            nextchar = ''
        return nextchar, end

    s, end = s_and_end
    pairs = []
    pairs_append = pairs.append

    # Use a slice to prevent IndexError from being raised, the following
    # check will raise a more specific ValueError if the string is empty
    nextchar = s[end:end + 1]
    # Normally we expect nextchar == '"'
    if nextchar != '"':
        if nextchar in _ws:
            end = _w(s, end).end()
            nextchar = s[end:end + 1]
        end = check_ellipsis(end)
        nextchar = s[end:end + 1]
        # Trivial empty object
        if nextchar == '}':
            if object_pairs_hook is not None:
                result = object_pairs_hook(pairs)
                return result, end + 1
            pairs = dict(pairs)
            if object_hook is not None:
                pairs = object_hook(pairs)
            return pairs, end + 1
        elif nextchar != '"':
            raise ValueError(decoder.errmsg(
                "Expecting property name enclosed in double quotes", s, end))
    end += 1
    while True:
        key, end = decoder.py_scanstring(s, end, strict=strict)

        # To skip some function call overhead we optimize the fast paths where
        # the JSON key separator is ": " or just ":".
        if s[end:end + 1] != ':':
            end = _w(s, end).end()
            if s[end:end + 1] != ':':
                raise ValueError(decoder.errmsg("Expecting ':' delimiter",
                                                s, end))
        end += 1

        try:
            if s[end] in _ws:
                end += 1
                if s[end] in _ws:
                    end = _w(s, end + 1).end()
        except IndexError:
            pass

        try:
            value, end = scan_once(s, end)
        except StopIteration:
            raise ValueError(decoder.errmsg("Expecting object", s, end))
        pairs_append((key, value))

        try:
            nextchar = s[end]
            if nextchar in _ws:
                end = _w(s, end + 1).end()
                nextchar = s[end]
        except IndexError:
            nextchar = ''
        end += 1

        if nextchar == '}':
            break
        elif nextchar != ',':
            raise ValueError(decoder.errmsg("Expecting ',' delimiter",
                                            s, end - 1))
        nextchar, end = consume_whitespace(end)
        end = check_ellipsis(end)
        nextchar, end = consume_whitespace(end)

        end += 1
        if nextchar == '}':
            break

        if nextchar != '"':
            raise ValueError(decoder.errmsg(
                "Expecting property name enclosed in double quotes",
                s, end - 1))
    if object_pairs_hook is not None:
        result = object_pairs_hook(pairs)
        return result, end
    pairs = dict(pairs)
    if object_hook is not None:
        pairs = object_hook(pairs)
    return pairs, end

ELLIPSIS = re.compile(r'\.\.\.(?:\((\d+)\))?')

def _JSONArray(s_and_end, scan_once, _w=decoder.WHITESPACE.match,
               _ws=decoder.WHITESPACE_STR):
    s, end = s_and_end
    values = []
    nextchar = s[end:end + 1]
    if nextchar in _ws:
        end = _w(s, end + 1).end()
        nextchar = s[end:end + 1]
    # Look-ahead for trivial empty array
    if nextchar == ']':
        return values, end + 1
    _append = values.append
    while True:
        m = ELLIPSIS.match(s[end:])
        if m is not None:
            count = 1 if m.group(1) is None else int(m.group(1))
            values.extend((Ellipsis,) * count)
            end += m.end()
        else:
            try:
                value, end = scan_once(s, end)
            except StopIteration:
                raise ValueError(decoder.errmsg("Expecting object", s, end))
            _append(value)
        nextchar = s[end:end + 1]
        if nextchar in _ws:
            end = _w(s, end + 1).end()
            nextchar = s[end:end + 1]
        end += 1
        if nextchar == ']':
            break
        elif nextchar != ',':
            raise ValueError(decoder.errmsg("Expecting ',' delimiter", s, end))
        try:
            if s[end] in _ws:
                end += 1
                if s[end] in _ws:
                    end = _w(s, end + 1).end()
        except IndexError:
            pass

    return values, end

# ----------------------------------------------------------------------

def fill_in_ellipses(struc, left_part, right_part):
    '''Replace Ellipsis objects parsed out of a udiff with elements
    from struc.'''
    diff = []
    for path in all_paths(right_part):
        try:
            left_sub_struc = follow_path(left_part, path)
        except (IndexError, KeyError, TypeError):
            left_sub_struc = {}
        right_sub_struc = follow_path(right_part, path)
        if right_sub_struc is Ellipsis:
            diff.append([path, copy.deepcopy(follow_path(struc, path))])
        elif isinstance(right_sub_struc, dict) and Ellipsis in right_sub_struc:
            del right_sub_struc[Ellipsis]
            struc_dict = follow_path(struc, path)
            sd_keys = compute_keysets(struc_dict, right_sub_struc)[1]
            for key in sd_keys:
                if key not in left_sub_struc:
                    sub_path = path + [key]
                    diff.append([path + [key],
                                 copy.deepcopy(follow_path(struc, sub_path))])
    return patch(right_part, diff)

def split_udiff_parts(udiff):
    '''Split ``udiff`` into parts representing subsets of the left and
    right structures that were used to create it.

    The return value is a 2-tuple ``(left_json, right_json)``.  If
    ``udiff`` is a string representing a valid udiff, then each member of
    the tuple will be a structure formatted in the superset of JSON that
    can be interpreted using :func:`extended_json_decoder()`.

    The function itself works by stripping off the first character of
    every line in the udiff, and composing ``left_json`` out of those
    lines which begin with ``' '`` or ``'-'``, and ``right_json`` out
    of those lines which begin with ``' '`` or ``'+'``.

    >>> udiff = """--- <stdin>[0]
    ... +++ <stdin>[1]
    ...  {
    ...   "foo": "bar",
    ...   ...
    ...   "baz":
    ... -  "quux",
    ... +  "quordle",
    ...
    ... - "bar": null
    ...
    ... + "quux": false
    ...  }"""
    >>> left_json = """{
    ...  "foo": "bar",
    ...  ...
    ...  "baz":
    ...   "quux",
    ...  "bar": null
    ... }"""
    >>> right_json = """{
    ...  "foo": "bar",
    ...  ...
    ...  "baz":
    ...   "quordle",
    ...  "quux": false
    ... }"""
    >>> split_udiff_parts(udiff) == (left_json, right_json)
    True
    '''
    out_json_seq = udiff.split('\n')
    if out_json_seq[0][:3] == '---' and out_json_seq[1][:3] == '+++':
        out_json_seq = out_json_seq[2:]
    left_json = (line[1:] for line in out_json_seq if line and line[0] != '+')
    right_json = (line[1:] for line in out_json_seq if line and line[0] != '-')
    return '\n'.join(left_json), '\n'.join(right_json)
