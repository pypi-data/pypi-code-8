from configwrapper import ValidationError
from configwrapper.section import ConfigOption

__author__ = 'Lai Tash (lai.tash@yandex.ru)'


class StringOption(ConfigOption):
    def _validate_serialized(self, string_):
        return

    def _validate_value(self, value):
        if not isinstance(value, str):
            raise ValidationError('string value expected')

    def serialize(self, value, instance):
        if value == '""':
            return '""'
        elif value == "''":
            return "\"''\""
        if not value:
            return '""'
        return value

    def deserialize(self, string_, instance):
        if string_ == "''":
            return ''
        else:
            return string_