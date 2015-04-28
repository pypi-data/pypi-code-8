"""
Deprecated components that will be removed before v1.0
"""


import warnings

try:  # pragma no cover
    import click
except ImportError:  # pragma no cover
    warnings.warn('Could not import `click` - some functions may not work')

from . import ext


__all__ = ['click_callback_key_val_dict', 'click_callback']


def click_callback_key_val_dict(ctx, param, value):

    """
    DEPRECATED - Use `str2type.ext.click_cb_key_val()` instead.

    Some options like `-ro` take `key=val` pairs that need to be transformed
    into `{'key': 'val}`.  This function can be used as a callback to handle
    all options for a specific flag, for example if the user specifies 3 reader
    options like `-ro key1=val1 -ro key2=val2 -ro key3=val3` then `click` uses
    this function to produce `{'key1': 'val1', 'key2': 'val2', 'key3': 'val3'}`.
    Parameters
    ----------
    ctx : click.Context
        Ignored
    param : click.Option
        Ignored
    value : tuple
        All collected key=val values for an option.
    Returns
    -------
    dict
    """

    warnings.warn(
        "`str2type.click_callback_key_val_dict()` is deprecated and will be removed before "
        "v1.0.  Switch to `str2type.ext.click_cb_key_val()`.", FutureWarning, stacklevel=2
    )

    try:
        return ext.click_cb_key_val(ctx=ctx, param=param, value=value)
    except click.BadParameter as e:
        raise ValueError(e)


def click_callback(ctx, param, value):

    warnings.warn(
        "`str2type.click_callback()` is deprecated and will be removed before "
        "v1.0.  Switch to `str2type.ext.click_callback()`.", FutureWarning, stacklevel=2
    )

    return ext.click_cb(ctx, param, value)
