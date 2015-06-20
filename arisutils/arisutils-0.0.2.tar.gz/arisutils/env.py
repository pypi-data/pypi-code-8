from distutils.util import strtobool
from os import environ

from .exceptions import ImproperlyConfigured


__no_default = object()

def _get_cast(key, default, cast):
    if cast is None:
        if default is not __no_default:
            if default is None:
                raise ImproperlyConfigured("%s has default type None, cast type is required but missing" % key)
            cast = type(default)
        else:
            cast = str

    if (default not in (None, __no_default)) and (type(default) != cast):
        msg = "%s has default %s %s, which does not match cast type %s"
        raise ImproperlyConfigured(msg % (key, default, type(default), cast))

    if cast == bool:
        cast = lambda val: bool(strtobool(val))

    return cast


def env(key, default=__no_default, cast=None, allow_blank=False):
    cast = _get_cast(key, default, cast)

    try:
        value = environ[key]
    except KeyError:
        if default is not __no_default:
            return default
        raise ImproperlyConfigured("%s must be in environment" % key)

    if value == '':
        if not allow_blank:
            raise ImproperlyConfigured("%s cannot be blank ('')" % key)

    try:
        return cast(value)
    except ValueError:
        raise ImproperlyConfigured("%s=%s cannot be cast to %s" % (key, value, cast))
