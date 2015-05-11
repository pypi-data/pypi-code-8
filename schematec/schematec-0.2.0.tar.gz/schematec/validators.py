from __future__ import absolute_import

import collections

import schematec.exc as exc


class Validator(object):
    BINDING = None


class Required(Validator):
    def __call__(self, name, data):
        if name not in data:
            raise exc.ValidationError(name)

required = Required()


class Length(Validator):
    BINDING = (str, collections.Sized)

    def __init__(self, max_length):
        self.max_length = max_length

    def __call__(self, value):
        if len(value) > self.max_length:
            raise exc.ValidationError(value)

length = Length
