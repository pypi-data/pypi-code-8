# -*- encoding: utf-8 -*-
# json_delta: a library for computing deltas between JSON-serializable
# structures.
# json_delta/_patch.py
#
# Copyright 2012‒2015 Philip J. Roberts <himself@phil-roberts.name>.
# BSD License applies; see the LICENSE file, or
# http://opensource.org/licenses/BSD-2-Clause
'''Functions for applying JSON-format patches.'''
from __future__ import unicode_literals
import copy

def patch(struc, diff, in_place=True):
    '''Apply the sequence of diff stanzas ``diff`` to the structure
    ``struc``.

    By default, this function modifies ``struc`` in place; set
    ``in_place`` to ``False`` to return a patched copy of struc
    instead.
    '''
    if not in_place:
        struc = copy.deepcopy(struc)
    for stanza in diff:
        struc = patch_stanza(struc, stanza)
    return struc

def patch_stanza(struc, diff):
    '''Applies the diff stanza ``diff`` to the structure ``struc`` as
    a patch.

    Note that this function modifies ``struc`` in-place into the
    target of ``diff``.'''
    changeback = False
    if type(struc) is tuple:
        changeback = True
        struc = list(struc)[:]
    key = diff[0]
    if not key:
        struc = diff[1]
        changeback = False
    elif len(key) == 1:
        if len(diff) == 1:
            del struc[key[0]]
        elif (type(struc) in (list, tuple)) and key[0] == len(struc):
            struc.append(diff[1])
        else:
            struc[key[0]] = diff[1]
    else:
        pass_key = key[:]
        pass_struc_key = pass_key.pop(0)
        pass_struc = struc[pass_struc_key]
        pass_diff = [pass_key] + diff[1:]
        struc[pass_struc_key] = patch_stanza(pass_struc, pass_diff)
    if changeback:
        struc = tuple(struc)
    return struc

