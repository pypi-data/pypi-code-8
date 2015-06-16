from configwrapper.section import ConfigSection

__author__ = 'Lai Tash (lai.tash@yandex.ru)'


#class _ConfigSchemaMeta(type):
#    def __init__(cls, *args, **kwargs):
#        for key, member in cls.__dict__.iteritems():
#            if (isinstance(member, type) and
#                    issubclass(member, ConfigSection)):
#                obj = member()
#                obj.schema = cls
#                setattr(cls, key, )


class ConfigSchema(object):

    allow_undefined = False

    def __init__(self, config, allow_undefined=None, **sections):
        self.config = config
        for name in dir(self):
            member = getattr(self, name)
            if isinstance(member, type) and issubclass(member, ConfigSection):
                obj = member()
                obj.bind(schema=self)
                if obj.prefix is None:
                    obj.bind(prefix=name)
                setattr(self, name, obj)
            elif isinstance(member, ConfigSection):
                member.bind(schema=self)
                if member.prefix is None:
                    member.bind(prefix=name)
        for key, section in sections.iteritems():
            section.bind(schema=self)
            if section.prefix is None:
                section.bind(prefix=key)
            setattr(self, key, section)

    @property
    def defined_sections(self):
        for key in dir(self):
            member = getattr(self, key)
            if isinstance(member, ConfigSection):
                yield member