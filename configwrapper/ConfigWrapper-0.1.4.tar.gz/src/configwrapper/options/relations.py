from ConfigParser import NoSectionError
from configwrapper import ValidationError
from configwrapper.options import ConfigOption
from configwrapper.section import ConfigSection

__author__ = 'Lai Tash (lai.tash@yandex.ru)'


class SectionOption(ConfigOption):
    def __init__(self, section=None, *args, **kwargs):
        self.section_cls = section
        super(SectionOption, self).__init__(*args, **kwargs)

    def _get_default(self, instance):
        if self.default is not None:
            return self.default
        return self.deserialize('', instance)

    def deserialize(self, value, instance=None):
        suffix = value
        section_cls = self.section_cls or self.name
        if isinstance(section_cls, basestring):
            try:
                section = getattr(instance.schema, section_cls)
            except AttributeError:
                raise NoSectionError(section_cls)
        else:
            section = section_cls
        if not isinstance(section, ConfigSection):
            raise ValidationError('Not a section"')
        return section[suffix].bind(schema=instance.schema)

    def serialize(self, value, instance=None):
        return value.suffix

    def _validate_serialized(self, string_):
        pass

    def _validate_value(self, value):
        return isinstance(value, ConfigSection)