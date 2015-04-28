"""
Unittests for: str2type.core
"""


import codecs
import json
import os

from nose.tools import assert_raises

import str2type


def test_valid_types():
    assert str2type.str2type("TrUe") is True
    assert str2type.str2type("FaLsE") is False
    assert str2type.str2type("NoNe") is None
    assert str2type.str2type("123") is 123
    assert str2type.str2type("1.23") == 1.23
    assert str2type.str2type("Some string") == "Some string"
    s = '{"K3": [0, 1, 2, 3, 4], "UPPERCASE": "v2", "k1": "MORE UPPERCASE"}'
    assert str2type.str2type(s) == json.loads(s)
    s = '{"k3": [0, 1, 2, 3, 4], "k2": "v2", "k1": "v1"}'
    assert str2type.str2type(s[1:]) == s[1:]
    s = '1.'
    assert str2type.str2type(s) == float(s)
    s = '.1'
    assert str2type.str2type(s) == float(s)
    s = 'nul'
    assert str2type.str2type(s) == s


def test_invalid_type():
    with assert_raises(TypeError):
        str2type.str2type(None)


def test_decode_escape():
    s = codecs.encode(os.linesep, 'unicode_escape')
    assert str2type.str2type(s) == os.linesep


def test_no_decode_escape():
    s = str(codecs.encode(os.linesep, 'unicode_escape'))
    assert str2type.str2type(s, decode_escape=False) == s
