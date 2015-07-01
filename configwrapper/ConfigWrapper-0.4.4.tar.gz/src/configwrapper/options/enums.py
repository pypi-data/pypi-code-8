from configwrapper.section import ConfigOption

__author__ = 'Lai Tash (lai.tash@yandex.ru)'


class EnumOption(ConfigOption):
    def __init__(self, enum, *args, **kwargs):
        self.enum = enum if isinstance(enum, dict) else {i: i for i in enum}
        super(EnumOption, self).__init__(*args, **kwargs)

    def deserialize(self, string_, instance):
        return self.enum[string_]

    def serialize(self, value, instance):
        return {v: k for k, v in self.enum.iteritems()}[value]

    def _validate_serialized(self, string_):
        return string_ in self.enum

    def _validate_value(self, value):
        return value in self.enum.values()