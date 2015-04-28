"""
Unittests for: str2type.deprecated
"""


import warnings

import str2type
from .data import TYPE_LOOP

from nose.tools import assert_raises


warnings.filterwarnings('ignore')


def test_click_callback_key_val_to_dict():
    content = ['key1=NOnE', 'key2=1', 'key4=1.']
    expected = {param.split('=')[0]: str2type.str2type(param.split('=')[1]) for param in content}
    result = str2type.click_callback_key_val_dict(None, None, content)
    assert isinstance(result, dict)
    assert len(result) is len(content)
    for key, val in result.items():
        assert val == expected[key], "Expected: `%s' - Actual: `%s'" % (expected[key], val)


def test_click_callback_key_val_to_dict_bad_format():
    with assert_raises(ValueError):
        str2type.click_callback_key_val_dict(None, None, ('good=formatting', 'bad_formatting'))


def test_click_callback():
    for val, cast in TYPE_LOOP:
        assert str2type.click_callback(None, None, val) == cast(val)


def test_backwards_dotted_lookup():
    for attr in ('str2type', 'click_callback', 'click_callback_key_val_dict'):
        assert hasattr(str2type, attr)
        assert hasattr(getattr(str2type, attr), '__call__')
