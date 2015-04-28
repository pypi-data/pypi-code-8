"""
Extensions for specific modules.

- click: https://github.com/mitsuhiko/click
"""


import click

from .core import str2type


__all__ = ['click_cb', 'click_cb_key_val', 'ClickStr2Type']


def click_cb(ctx, param, value):

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


def click_cb_key_val(ctx, param, value):

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
            if key in output:
                raise click.BadParameter(
                    'key specified multiple times for KEY=VAL argument: `%s' % key)
            val = str2type(val)
            output[key] = val

    return output


class ClickStr2Type(click.ParamType):

    """
    A type class for use with click that only wraps `str2type()`.  Using `click_cb()` as
    a callback has the same effect.

    https://github.com/mitsuhiko/click
    """

    def convert(self, value, param, ctx):
        try:
            return str2type(value)
        except Exception as e:
            self.fail('encountered an exception while decoding string: %s'
                      % repr(e), param=param, ctx=ctx)
