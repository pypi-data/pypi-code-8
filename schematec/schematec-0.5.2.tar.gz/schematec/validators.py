from __future__ import absolute_import

import collections

import schematec.exc as exc
import schematec.abc as abc


class Required(abc.UnboundValidator):
    def __call__(self, name, data):
        if name not in data:
            raise exc.ValidationError(name)

required = Required()


class Length(abc.BoundValidator):
    BINDING = (str, collections.Sized)

    def __init__(self, max_length):
        self.max_length = max_length

    def __call__(self, value):
        if len(value) > self.max_length:
            raise exc.ValidationError(value)

length = Length


class Regex(abc.BoundValidator):
    BINDING = (str, )

    def __init__(self, regex):
        self.regex = regex

    def __call__(self, value):
        if not self.regex.match(value):
            raise exc.ValidationError(value)

regex = Regex
