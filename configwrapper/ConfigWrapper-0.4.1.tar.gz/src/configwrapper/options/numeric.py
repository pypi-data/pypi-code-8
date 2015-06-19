from decimal import Decimal, InvalidOperation
from configwrapper import ValidationError
from configwrapper.section import ConfigOption

__author__ = 'Lai Tash (lai.tash@yandex.ru)'


class IntOption(ConfigOption):
    def __init__(self, allow=None, *args, **kwargs):
        self.allow = allow or (lambda i: True)
        super(IntOption, self).__init__(*args, **kwargs)

    def _validate_value(self, value):
        if not isinstance(value, int):
            raise ValidationError('Integer value expected')
        if not self.allow(value):
            raise ValidationError('Value is not allowed')

    def _validate_serialized(self, string_):
        if not string_.isdigit():
            raise ValidationError('Integer value expected')

    def serialize(self, value, instance):
        return str(value)

    def deserialize(self, string_, instance):
        return int(string_)


class DecimalOption(IntOption):
    def _validate_value(self, value):
        if not isinstance(value, (Decimal, int, long)):
            raise ValidationError('Decimal value expected')
        if not self.allow(value):
            raise ValidationError('Value is not allowed')

    def _validate_serialized(self, string_):
        try:
            Decimal(string_)
        except InvalidOperation:
            raise ValidationError('Decimal value expected')


    def serialize(self, value, instance):
        return str(value)

    def deserialize(self, string_, instance):
        return Decimal(string_)


class FloatOption(IntOption):
    def _validate_value(self, value):
        if not isinstance(value, (float, Decimal, int, long)):
            raise ValidationError('Numeric value expected')
        if not self.allow(value):
            raise ValidationError('Value is not allowed')

    def _validate_serialized(self, string_):
        try:
            Decimal(string_)
        except InvalidOperation:
            raise ValidationError('Decimal value expected')

    def serialize(self, value, instance):
        return str(value)

    def deserialize(self, string_, instance):
        return float(string_)