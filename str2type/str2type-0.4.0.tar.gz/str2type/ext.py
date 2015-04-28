"""
Extensions for specific modules.

- click: https://github.com/mitsuhiko/click
"""


import click

from .core import str2type


def click_callback(ctx, param, value):

    """
    Easily integrate `str2type()` into the CLI framework click as a callback
    function to automatically cast commandline arguments to their native Python
    type.  Click already handles this but sometimes values can be of multiple,
    especially for `key=val` arguments that will be passed to a class as
    `**kwargs`.

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

    return str2type(value)


def click_callback_key_val_dict(ctx, param, value):

    """
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

    output = {}
    for pair in value:
        if '=' not in pair:
            raise click.BadParameter("incorrect syntax for KEY=VAL argument: `%s'" % pair)
        else:
            key, val = pair.split('=')
            val = str2type(val)
            output[key] = val

    return output
