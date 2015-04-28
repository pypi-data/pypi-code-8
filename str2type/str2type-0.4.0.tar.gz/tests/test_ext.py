"""
Unittests for: str2type.click_extensions
"""


import click
from nose.tools import assert_raises

import str2type.ext
from .data import TYPE_LOOP


def test_click_callback_key_val_to_dict():
    content = ['key1=NOnE', 'key2=1', 'key4=1.']
    expected = {param.split('=')[0]: str2type.str2type(param.split('=')[1]) for param in content}
    result = str2type.ext.click_callback_key_val_dict(None, None, content)
    assert isinstance(result, dict)
    assert len(result) is len(content)
    for key, val in result.items():
        assert val == expected[key], "Expected: `%s' - Actual: `%s'" % (expected[key], val)


def test_click_callback_key_val_to_dict_bad_format():
    with assert_raises(click.BadParameter):
        str2type.ext.click_callback_key_val_dict(None, None, ('good=formatting', 'bad_formatting'))


def test_click_callback():
    for val, cast in TYPE_LOOP:
        assert str2type.ext.click_callback(None, None, val) == cast(val)
