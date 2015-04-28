"""
Unittests for: str2type.click_extensions
"""


import click
from nose.tools import assert_raises

import str2type.ext
from .data import TYPE_LOOP


def test_click_callback_key_val_to_dict():
    content = ['key1=NOnE', 'key2=1', 'key4=1.']
    expected = {
        param.split('=')[0]: str2type.str2type(param.split('=')[1]) for param in content}
    result = str2type.ext.click_cb_key_val(None, None, content)
    assert isinstance(result, dict)
    assert len(result) is len(content)
    for key, val in result.items():
        assert val == expected[key], "Expected: `%s' - Actual: `%s'" % (expected[key], val)


def test_click_callback_key_val_to_dict_bad_format():
    with assert_raises(click.BadParameter):
        str2type.ext.click_cb_key_val(
            None, None, ('good=formatting', 'bad_formatting'))
    # Key specified multiple times
    with assert_raises(click.BadParameter):
        str2type.ext. click_cb_key_val(None, None, ('key=val', 'key=val'))


def test_click_callback():
    for val, cast in TYPE_LOOP:
        assert str2type.ext.click_cb(None, None, val) == cast(val)


def test_click_type_class():
    type_class = str2type.ext.ClickStr2Type()
    assert isinstance(type_class, click.ParamType)
    assert type_class.convert(ctx=None, param=None, value='1') is 1
    for string, validate in TYPE_LOOP:
        assert type_class.convert(
            ctx=None, param=None, value=string) == validate(string), string
    with assert_raises(click.BadParameter):
        type_class.convert(ctx=None, param=None, value=str2type)
