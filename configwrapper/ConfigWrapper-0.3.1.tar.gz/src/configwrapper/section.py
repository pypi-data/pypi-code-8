from ConfigParser import NoOptionError
from configwrapper import ValidationError
from configwrapper.options import ConfigOption

__author__ = 'Lai Tash (lai.tash@yandex.ru)'


class SectionError(Exception):
    pass



class _ConfigSectionMeta(type):
    def __init__(cls, name, bases, dct):
        super(_ConfigSectionMeta, cls).__init__(name, bases, dct)
        for k, member in dct.iteritems():
             if isinstance(member, ConfigOption):
                 if getattr(member, 'config_name', None) is None:
                     member.name = k

class ConfigSection(object):
    __metaclass__ = _ConfigSectionMeta

    allow_undefined = None
    prefix = None
    implicit_options = {}

    def __init__(self, allow_undefined=None, **options):
        self.implicit_options = {}
        for key, value in options.iteritems():
            if isinstance(value, ConfigOption):
                self.implicit_options[key] = value
            else:
                setattr(self, key, value)
        if allow_undefined is not None:
            self.allow_undefined = allow_undefined
        self.schema = None

        for key, option in self.implicit_options.iteritems():
            if option.name is None:
                option.name = key

    def bind(self, schema=None, prefix=None):
        if schema:
            self.schema = schema
        if prefix:
            self.prefix = prefix
        return self

    @property
    def config(self):
        return self.schema.config

    @property
    def config_name(self):
        return self.prefix

    @property
    def options(self):
        for member in dir(self):
            if isinstance(member, ConfigOption):
                yield getattr((ConfigSection, self), member)
        for option in self.implicit_options:
            yield self.implicit_options[option]

    @property
    def option_dict(self):
        result = {option.name: option for option in self.options}
        return result

    @property
    def values(self):
        return self.config.items(self.config_name)

    def match_name(self, name):
        if name == self.prefix:
            return self

    def __getattr__(self, item):
        try:
            return self.implicit_options[item].__get__(self, self.__class__)
        except KeyError:
            member = getattr(self.__class__, item)
            if hasattr(member, '__get__'):
                return member.__get__(self, self.__class__)
            else:
                return member

    def __setattr__(self, key, value):
        option = self.option_dict.get(key, None)
        if option is not None:
            option.__set__(self, value)
            return
        else:
            super(ConfigSection, self).__setattr__(key, value)

    def get_serialized(self, option):
        return self.config.get(self.config_name, option)

    def set_serialized(self, option, value):
        self.config.set(self.prefix, option, value)

    def validate(self):
        for name, value in self.values:
            if name in self.option_dict:
                self.option_dict[name].validate(self, value)
            elif not self.allow_undefined:
                raise ValidationError('Unknown option: %s' % name)


class TemplateSection(ConfigSection):
    def __init__(self, allow_undefined=None, parent=None, **options):
        self.parent = parent
        self.suffix = None
        super(TemplateSection, self).__init__(allow_undefined, **options)

    def __eq__(self, other):
        return (self.schema == other.schema and
                self.prefix == other.prefix and
                self.suffix == other.suffix)

    def match_name(self, name):
        if name.startswith('%s_' % self.prefix):
            return self[name[len(self.prefix)+1:]]
        else:
            return super(TemplateSection, self).match_name(name)

    def bind(self, schema=None, prefix=None, suffix=None):
        super(TemplateSection, self).bind(schema, prefix)
        if suffix is not None:
            self.suffix = suffix
        return self

    def _suffixed_name(self):
        return '%s_%s' % (self.prefix, self.suffix)

    @property
    def config_name(self):
        return self.prefix if not self.suffix else self._suffixed_name()

    def __getitem__(self, item):
        if self.suffix:
            raise SectionError('Not a parent section')
        result = self.__class__(
            self.allow_undefined, self, **self.implicit_options)
        result.bind(schema=self.schema, prefix=self.prefix, suffix=item)
        result.schema = self.schema
        return result

    def get_serialized(self, option):
        super_obj = super(TemplateSection, self)
        if self.suffix:
            try:
                super_obj.get_serialized(option)
            except NoOptionError:
                return self.parent.get_serialized(option)
        return super(TemplateSection, self).get_serialized(option)


