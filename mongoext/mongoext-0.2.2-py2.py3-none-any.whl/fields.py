from __future__ import absolute_import

import collections
import datetime


def required(fn):
    def wrapper(self, val):
        if val is None and self.required:
            raise ValueError('Required')
        return fn(self, val)
    return wrapper


class Field(object):
    def __init__(self, required=False):
        self.required = required

    @required
    def __call__(self, val):
        return val


class String(Field):
    @required
    def __call__(self, val):
        try:
            return unicode(val)
        except TypeError:
            raise ValueError('String is required')


class Numeric(Field):
    @required
    def __call__(self, val):
        try:
            return int(val)
        except (TypeError, ValueError):
            raise ValueError('Integer is required')


class List(Field):
    def __init__(self, field=None, required=False):
        if field and not isinstance(field, Field):
            raise ValueError
        self.field = field
        self.required = required

    @required
    def __call__(self, val):
        if not isinstance(val, collections.Iterable):
            raise ValueError('Iterablerequired')
        if self.field:
            return [self.field(v) for v in val]
        else:
            return list(val)


class DateTime(Field):
    def __init__(self, required=False, autoadd=False):
        self.required = required
        self.autoadd = autoadd

    @required
    def __call__(self, val):
        if self.autoadd:
            val = datetime.datetime.now()
        if not isinstance(val, datetime.datetime):
            raise ValueError('Datetime objectrequired')
        return val


class Dict(Field):
    def __init__(self, field=None, required=False):
        if field and not isinstance(field, Field):
            raise ValueError
        self.field = field
        self.required = required

    @required
    def __call__(self, val):
        if not isinstance(val, collections.Mapping):
            raise ValueError('Mapping object required')
        if self.field:
            return {k: self.field(v) for k, v in val.items()}
        else:
            return dict(val)
