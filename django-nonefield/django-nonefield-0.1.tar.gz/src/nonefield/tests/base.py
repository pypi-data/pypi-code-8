from __future__ import print_function

__title__ = 'nonefield.tests.base'
__author__ = 'Artur Barseghyan <artur.barseghyan@gmail.com>'
__copyright__ = 'Copyright (c) 2015 Artur Barseghyan'
__license__ = 'GPL 2.0/LGPL 2.1'
__all__ = ('PRINT_INFO', 'print_info', 'OPTIONAL_SKIP', 'optional_skip',)

# ****************************************************************************
# ****************************************************************************
# ****************************************************************************

PRINT_INFO = True
TRACK_TIME = False

def print_info(func):
    """
    Prints some useful info.
    """
    if not PRINT_INFO:
        return func

    def inner(self, *args, **kwargs):

        result = func(self, *args, **kwargs)

        print('\n{0}'.format(func.__name__))
        print('============================')
        if func.__doc__:
            print('""" {0} """'.format(func.__doc__.strip()))
        print('----------------------------')
        if result is not None:
            print(result)
        print('\n')

        return result
    return inner

OPTIONAL_SKIP = False

def optional_skip(func):
    """
    Simply skips the test.
    """
    def inner(self, *args, **kwargs):
        if OPTIONAL_SKIP:
            return
        return func(self, *args, **kwargs)
    return inner
