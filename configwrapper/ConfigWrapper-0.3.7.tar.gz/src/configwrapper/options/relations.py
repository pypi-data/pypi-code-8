from ConfigParser import NoSectionError
from configwrapper import ValidationError
from configwrapper.section import ConfigSection, ConfigOption

__author__ = 'Lai Tash (lai.tash@yandex.ru)'


class SectionOption(ConfigOption):
    def __init__(self, section=None, *args, **kwargs):
        self.section_cls = section
        super(SectionOption, self).__init__(*args, **kwargs)

    def _get_default(self, instance):
        if self.default is not None:
            return self.default
        return self.deserialize('', instance)

    def deserialize(self, string_, instance):
        suffix = string_
        section_cls = self.section_cls or self.name
        if isinstance(section_cls, basestring):
            try:
                section = getattr(instance.schema, section_cls)
            except AttributeError:
                raise NoSectionError(section_cls)
        else:
            section = section_cls
        if not isinstance(section, ConfigSection):
            if (isinstance(section, type) and
                    issubclass(section, ConfigSection)):
                section = section()
            else:
                raise ValidationError('Not a section"')
        return section[suffix].bind(schema=instance.schema)

    def serialize(self, value, instance):
        return value.suffix

    def _validate_serialized(self, string_):
        pass

    def _validate_value(self, value):
        return isinstance(value, ConfigSection)


class ObjectOption(ConfigOption):
    def __init__(self, factories, *args, **kwargs):
        self.factories = factories
        super(ObjectOption, self).__init__(*args, **kwargs)

    def _get_default(self, instance):
        if self.default is not None:
            return self.create(self.default, instance)
        return self.deserialize('', instance)

    def create(self, factory, instance):
        return self.factories[factory](instance)

    def deserialize(self, string_, instance):
        return self.create(string_, instance)

    def serialize(self, value, instance):
        raise NotImplementedError()

    def _validate_serialized(self, string_):
        return string_ in self.factories

    def _validate_value(self, value):
        pass
