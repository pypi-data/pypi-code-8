from __future__ import absolute_import


class IDescriptor(object):
    pass


class Schema(IDescriptor):
    pass


class Converter(IDescriptor):
    pass


class Validator(IDescriptor):
    BINDING = None
