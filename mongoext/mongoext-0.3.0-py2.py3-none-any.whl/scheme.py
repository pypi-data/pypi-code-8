from __future__ import absolute_import

import collections
import datetime
import weakref

import mongoext.exc as exc


class Scheme(object):
    def __init__(self, fields):
        self.fields = fields

    def __contains__(self, field):
        return field in self.fields

    def __iter__(self):
        for field in self.fields:
            yield field

    def validate(self, document):
        for attr, field in self.fields.items():
            if field.required and getattr(document, attr) is None:
                raise exc.SchemeError('Required field is missing: {}'.format(attr))


class Field(object):
    def __init__(self, required=False):
        self.required = required

        self.data = weakref.WeakKeyDictionary()

    def __get__(self, instance, owner):
        return self.data.get(instance)

    def __set__(self, instance, value):
        value = self.cast(value)
        self.data[instance] = value

    def cast(self, value):
        return value


class Unicode(Field):
    def cast(self, val):
        ''' Cast value to unicode. '''
        try:
            return unicode(val)
        except TypeError:
            raise exc.CastError('String is required: {}'.format(val))


class Numeric(Field):
    def cast(self, val):
        ''' Cast value to unicode. '''
        try:
            return int(val)
        except (TypeError, ValueError):
            raise exc.CastError('Integer is required: {}'.format(val))


class List(Field):
    ''' Cast value to list. '''
    def __init__(self, field=None, **kw):
        super(List, self).__init__(**kw)

        if field and not isinstance(field, Field):
            raise exc.SchemeError('Field successor instance required: {}'.format(field))
        self.field = field

    def cast(self, val):
        if not isinstance(val, collections.Iterable):
            raise exc.CastError('Iterable object required')
        if self.field:
            return [self.field.cast(v) for v in val]
        else:
            return list(val)


class DateTime(Field):
    def __init__(self, autoadd=False, **kw):
        super(DateTime, self).__init__(**kw)

        self.autoadd = autoadd

    def cast(self, val):
        if self.autoadd:
            val = datetime.datetime.now()
        if not isinstance(val, datetime.datetime):
            raise exc.CastError('Datetime object required')
        return val


class Dict(Field):
    def __init__(self, field=None, **kw):
        super(Dict, self).__init__(**kw)

        if field and not isinstance(field, Field):
            raise exc.SchemeError('Field successor instance required: {}'.format(field))
        self.field = field

    def cast(self, val):
        if not isinstance(val, collections.Mapping):
            raise exc.CastError('Mapping object required')
        if self.field:
            return {k: self.field.cast(v) for k, v in val.items()}
        else:
            return dict(val)
