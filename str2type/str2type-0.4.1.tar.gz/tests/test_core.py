"""
Unittests for: str2type.core
"""


import codecs
import json
import os

from nose.tools import assert_raises

import str2type


def test_valid_types():
    for s in ('TrUe', 'FaLsE', 'NoNe', 'null', 'nul'):
        assert str2type.str2type(s) == s
    for check, val in (
            (float, '1.'), (float, '.1'), (int, '123'), (float, '1.23'), (str, 'Some string'),
            (json.loads, '{"K3": [0, 1, 2, 3, 4], "UPPERCASE": "v2"}'),
            (json.loads, '{"k3": [0, 1, 2, 3, 4], "k2": "v2", "k1": "v1"}')
    ):
        assert str2type.str2type(val) == check(val)


def test_invalid_type():
    with assert_raises(TypeError):
        str2type.str2type(None)


def test_decode_escape():
    s = codecs.encode(os.linesep, 'unicode_escape')
    assert str2type.str2type(s) == os.linesep


def test_no_decode_escape():
    s = str(codecs.encode(os.linesep, 'unicode_escape'))
    assert str2type.str2type(s, decode_escape=False) == s
