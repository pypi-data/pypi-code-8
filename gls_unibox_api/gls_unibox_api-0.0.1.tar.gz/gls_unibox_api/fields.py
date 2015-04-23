# -*- coding: utf-8 -*-
"""
    fields.py

    Implemented a field descriptor
"""
import datetime
import decimal


class BaseField(object):
    def __init__(self, code, length=None):
        self.code = code
        self.length = length

    def __get__(self, obj, type=None):
        if type is None or obj is None:
            return self
        return self._from_string(
            obj.values.get(self.code)
        )

    def __set__(self, obj, value):
        if self.length is not None and \
                len(unicode(value)) > self.length:
            raise ValueError(
                'Length of %s cannot be more than %d' % (
                    self.code, self.length
                )
            )
        obj.values[self.code] = self._to_string(value)

    def __delete__(self, obj):
        if not self.mutable:
            raise RuntimeError('You cannot delete this field')
        obj.values.pop(self.code, None)

    def _from_string(self, raw_value):
        if raw_value is not None:
            return self.from_string(raw_value)

    def from_string(self, raw_value):
        return unicode(raw_value.decode('ISO-8859-1'))

    def _to_string(self, value):
        if value is not None:
            return self.to_string(value)

    def to_string(self, value):
        return unicode(value).encode('ISO-8859-1')


class Char(BaseField):
    pass


class Int(BaseField):

    def from_string(self, raw_value):
        return int(raw_value.decode('ISO-8859-1'))


class Long(BaseField):

    def from_string(self, raw_value):
        return long(raw_value.decode('ISO-8859-1'))


class Decimal(BaseField):
    def __init__(self, code, digits=(5, 1), **kwargs):
        self.digits = digits
        super(Decimal, self).__init__(code, **kwargs)

    def from_string(self, raw_value):
        return decimal.Decimal(
            raw_value.decode('ISO-8859-1').replace(',', '.')
        )

    def to_string(self, value):
        """
        Returns string representation of the field that can be sent over wire
        """
        return str(value).replace('.', ',')


class Date(BaseField):
    def __init__(self, code, separator='', **kwargs):
        """
        :param separator: Date separator
        """
        self.separator = separator
        super(Date, self).__init__(code, **kwargs)

    @property
    def format(self):
        return self.separator.join(('%d', '%m', '%Y'))

    def from_string(self, value):
        return datetime.datetime.strptime(value, self.format).date()

    def to_string(self, value):
        return value.strftime(self.format)


class Time(BaseField):

    def __init__(self, code, separator=':', **kwargs):
        """
        :param separator: Time separator
        """
        self.separator = separator
        super(Time, self).__init__(code, **kwargs)

    @property
    def format(self):
        return self.separator.join(('%H', '%M'))

    def from_string(self, value):
        return datetime.datetime.strptime(value, self.format).time()

    def to_string(self, value):
        return value.strftime(self.format)


class MultipleChoice(BaseField):

    def __init__(self, code, separator=';', **kwargs):
        """
        :param separator: separator that separates the parts
        """
        self.separator = separator
        super(MultipleChoice, self).__init__(code, **kwargs)

    @property
    def format(self):
        return self.separator.join(self.choices)

    def from_string(self, value):
        return value.split(self.separator)

    def to_string(self, value):
        return self.separator.join(value).encode('ISO-8859-1')


class FieldGroup(object):
    values = None

    def __get__(self, obj, type=None):
        if self.values is None and obj.values:
            self.values = obj.values
        return self
