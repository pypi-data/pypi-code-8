from abc import ABCMeta, abstractmethod
from ConfigParser import NoOptionError, NoSectionError
from configwrapper import ValidationError


class OptionError(Exception):
    def __init__(self, prefix, section, message):
        super(OptionError, self).__init__('[option %s from %s]: %s' %
                                          (prefix, section, message))


class ConfigOption(object):
    __metaclass__ = ABCMeta

    def __init__(self, name=None, nullable=False, mutable=False, default=None):
        """

        :param name: option name in configuration
        :param nullable: if True, value can be None
        :param mutable: if True, value can be changed at runtime
        """
        self.name = name
        self.nullable = nullable
        self.mutable = mutable
        if default is not None:
            self._validate_value(default)
        self.default = default

    def validate(self, instance, serialized=None):
        if serialized is None:
            serialized = instance.get_serialized(self.name)
        if not serialized:
            if not self.nullable:
                raise ValidationError(self, instance, 'is not nullable')
        self._validate_serialized(serialized)

    @abstractmethod
    def _validate_serialized(self, string_):
        """Test serialized value for error

        :raises OptionError: serialized value is invalid
        """
        pass

    @abstractmethod
    def _validate_value(self, value):
        """Test if value is a valid value for this option

        :raises OptionError: value is invalid
        """
        pass

    @abstractmethod
    def deserialize(self, string_, instance=None):
        pass

    @abstractmethod
    def serialize(self, value, instance=None):
        pass

    def _get_default(self, instance):
        result = self.default
        return result

    def __get__(self, instance, owner):
        if instance is None:
            return self._get_default(instance)
        try:
            serialized = instance.get_serialized(self.name)
        except (NoOptionError, NoSectionError):
            result = self._get_default(instance)
            self._validate_value(result)
            return result
        if not serialized:
            if not self.nullable:
                raise ValidationError('%s is not nullable' % self.name)
            return None
        result = self.deserialize(serialized, instance)
        self._validate_value(result)
        return result

    def __set__(self, instance, value):
        if not self.mutable:
            raise OptionError(self, instance, 'is not mutable')
        if value is None:
            if not self.nullable:
                raise OptionError(self, instance, 'is not nullable')
            string_ = ''
        else:
            self._validate_value(value)
            string_ = self.serialize(value, instance)
        instance.set_serialized(self.name, string_)