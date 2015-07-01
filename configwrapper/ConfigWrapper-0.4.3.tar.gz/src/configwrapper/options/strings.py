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


class UnicodeOption(StringOption):
    def __init__(self, encoding='utf-8', *args, **kwargs):
        self.encoding = encoding
        super(UnicodeOption, self).__init__(*args, **kwargs)

    def _validate_value(self, value):
        if not isinstance(value, unicode):
            raise ValidationError('unicode value expected')

    def serialize(self, value, instance):
        return super(UnicodeOption, self).serialize(value, instance).encode(
            self.encoding
        )

    def deserialize(self, string_, instance):
        result = super(UnicodeOption, self).deserialize(string_, instance)
        return result.decode(self.encoding)