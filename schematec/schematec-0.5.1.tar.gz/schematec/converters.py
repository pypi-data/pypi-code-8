from __future__ import absolute_import

import collections

import schematec.exc as exc
import schematec.abc as abc


class Integer(abc.Converter):
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

integer = Integer()


class Number(abc.Converter):
    def __call__(self, value):
        if value is None:
            raise exc.ConvertationError(value)

        if isinstance(value, bool):
            return float(value)

        if isinstance(value, (float, int, long)):
            return float(value)

        if isinstance(value, basestring):
            try:
                return float(value)
            except ValueError:
                raise exc.ConvertationError(value)

        raise exc.ConvertationError(value)

number = Number()


class String(abc.Converter):
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


class Boolean(abc.Converter):
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


class Array(abc.Converter):
    def __call__(self, value):
        if isinstance(value, collections.Iterable) and not isinstance(value, collections.Mapping):
            return list(value)

        raise exc.ConvertationError(value)

array = Array()


class Dictionary(abc.Converter):
    def __call__(self, value):
        if isinstance(value, collections.Mapping):
            return dict(value)

        raise exc.ConvertationError(value)

dictionary = Dictionary()
