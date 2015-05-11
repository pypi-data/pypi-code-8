'''
Convertaion rules
=================

Can be converted into:

numeric
-------

#. Any int or long value
#. Any suitable string/unicode
#. Boolean value

string
------

#. Any suitable string/unicode
#. Any int or long value

boolean
-------

#. Boolean value
#. 0 or 1
#. '0' or '1'
#. u'0' or u'1'

array
-----

#. Any iterable value(collections.Iterable)

dictionary
----------

#. Any mapping value(collections.Mapping)


'''
from __future__ import absolute_import

import collections

import schematec.exc as exc


class Converter(object):
    pass


class Numeric(Converter):
    def __call__(self, value):
        if value is None:
            raise exc.ConvertationError(value)

        if isinstance(value, bool):
            return int(value)

        if isinstance(value, (int, long)):
            return int(value)

        if isinstance(value, basestring):
            try:
                return int(value)
            except ValueError:
                raise exc.ConvertationError(value)

        raise exc.ConvertationError(value)

numeric = Numeric()


class String(Converter):
    def __call__(self, value):
        if value is None:
            raise exc.ConvertationError(value)

        if isinstance(value, unicode):
            return value

        if isinstance(value, bool):
            raise exc.ConvertationError(value)

        if isinstance(value, (int, long)):
            return unicode(value)

        if isinstance(value, str):
            try:
                return unicode(value)
            except UnicodeDecodeError:
                raise exc.ConvertationError(value)

        raise exc.ConvertationError(value)

string = String()


class Boolean(Converter):
    def __call__(self, value):
        if value is None:
            raise exc.ConvertationError(value)

        if isinstance(value, bool):
            return value

        if isinstance(value, (int, long)) and value in (0, 1):
            return bool(value)

        if isinstance(value, basestring) and value in (u'0', u'1'):
            return bool(int(value))

        raise exc.ConvertationError(value)

boolean = Boolean()


class Array(Converter):
    def __call__(self, value):
        if value is None:
            raise exc.ConvertationError(value)

        if isinstance(value, collections.Iterable):
            return list(value)

        raise exc.ConvertationError(value)

array = Array()


class Dictionary(Converter):
    def __call__(self, value):
        if value is None:
            raise exc.ConvertationError(value)

        if isinstance(value, collections.Mapping):
            return dict(value)

        raise exc.ConvertationError(value)

dictionary = Dictionary()
