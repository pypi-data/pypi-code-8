# coding=utf-8
from nekbot.core.exceptions import InvalidArgument

__author__ = 'nekmo'

class Person(object):
    pass


class Choice(object):
    def __init__(self, options):
        self.options = map(unicode.lower, options)

    def __call__(self, value):
        options = self.options
        if isinstance(value, unicode):
            options = map(unicode, options)
        if not value.lower() in options:
            raise InvalidArgument(u'the argument must be one of the following: %s' % ', '.join(options),
                                  value)
        return value


class Bool(Choice):
    CHOICES = {
        u'sí': True,
        u'no': False,
        u'n': False,
        u's': True,
        u'yes': True,
        u'y': True,
    }

    def __init__(self):
        Choice.__init__(self, self.CHOICES.keys())

    def __call__(self, value):
        value = Choice.__call__(self, value)
        return self.CHOICES[value]
Bool = Bool()