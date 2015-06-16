from configwrapper import ValidationError
from configwrapper.options import ConfigOption
from configwrapper.section import ConfigSection

__author__ = 'Lai Tash (lai.tash@yandex.ru)'


class StringOption(ConfigOption):
    def _validate_serialized(self, string_):
        return

    def _validate_value(self, value):
        if not isinstance(value, str):
            raise ValidationError('string value expected')

    def serialize(self, value, instance=None):
        if value == '""':
            return '""'
        elif value == "''":
            return "\"''\""
        if not value:
            return '""'
        return value

    def deserialize(self, string_, instance=None):
        if string_ == "''":
            return ''
        else:
            return string_


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
            raise ValidationError('String value expected')

    def serialize(self, value, instance=None):
        return str(value)

    def deserialize(self, string_, instance=None):
        return int(string_)


class OptionList(ConfigOption):
    def __init__(self, option, *args, **kwargs):
        self.option = option
        super(OptionList, self).__init__(*args, **kwargs)

    def deserialize(self, string_, instance=None):
        result = []
        items = map(str.strip, string_.split(','))
        for item in items:
            self.option.validate(item)
            result.append(self.option.deserialize(item))

    def serialize(self, value, instance=None):
        value = map(self.option.serialize, value)
        for item in value:
            self.option.validate(item)
        return value

    def _validate_value(self, value):
        if not isinstance(value, list):
            raise ValidationError('list expected')

    def _validate_serialized(self, string_):
        pass


class SectionOption(ConfigOption):
    def __init__(self, section, *args, **kwargs):
        self.section = section
        super(SectionOption, self).__init__(*args, **kwargs)

    def deserialize(self, value, instance=None):
        suffix = value
        return self.secton[suffix].bind(schema=instance.schema)

    def serialize(self, value, instance=None):
        return value.suffix

    def _validate_serialized(self, string_):
        pass

    def _validate_value(self, value):
        return isinstance(value, ConfigSection)


class EnumOption(ConfigOption):
    def __init__(self, enum, *args, **kwargs):
        self.enum = enum
        super(EnumOption, self).__init__(*args, **kwargs)

    def deserialize(self, string_, instance=None):
        return self.enum(string_)

    def serialize(self, value, instance=None):
        return {v: k for k, v in self.enum.iteritems()}[value]

    def _validate_serialized(self, string_):
        return string_ in self.enum

    def _validate_value(self, value):
        return value in self.enum.values()


class LinkArgument(ConfigOption):
    def serialize(self, value, instance=None):
        pass