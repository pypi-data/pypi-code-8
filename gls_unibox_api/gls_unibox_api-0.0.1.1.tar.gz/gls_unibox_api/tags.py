# -*- coding: utf-8 -*-
class TagMeta(type):
    """
    Metaclass for all Tags
    """
    def __new__(meta, name, bases, dct):
        if name != 'Tag':
            if 'code' not in dct:
                raise TypeError('code is not defined in tag: %s' % name)

            if 'description' not in dct:
                raise TypeError('description is not defined in tag: %s' % name)

            if 'max_length' in dct and \
                    not isinstance(dct['max_length'], (int, long)):
                raise TypeError(
                    'max_length: expected int or long. Got %s (%s)' % (
                        dct['max_length'], type(dct['max_length'])
                    )
                )

        return type.__new__(meta, name, bases, dct)


class Tag(object):
    """
    Base Tag related functionality
    """
    __metaclass__ = TagMeta

    def get_encoded_value(self):
        if not hasattr(self, 'value'):
            rv = self.code
        else:
            rv = '%s:%s' % (self.code, self.value)

        # Finally return the encoded value
        return rv.encode('ISO-8859-1')


class StartTag(Tag):
    "Start Tag of Datastream"
    code = '\\' * 5 + 'GLS' + '\\' * 5
    description = __doc__


class EndTag(Tag):
    "Start Tag of Datastream"
    code = '/' * 5 + 'GLS' + '/' * 5
    description = __doc__


class CancelParcel(Tag):
    "CANCELLATION for parcel number"
    code = 'T000'
    description = __doc__

    def __init__(self, parcel_number):
        self.value = parcel_number


class PrinterInterface(Tag):
    "Printer-interface, also for selection of the Default-interface"
    code = 'T020'
    description = __doc__
