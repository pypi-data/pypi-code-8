from ConfigParser import SafeConfigParser
from ConfigParser import NoOptionError
from ConfigParser import NoSectionError

import click
import six

from machinepack.core import MachinePackViewer
from machinepack import settings

class Echo(object):
    '''Object oriented wrapper around Click `secho` function.'''

    def __init__(self, debug=0):
        self.debug = debug

    def __call__(self, message, debug=None, **style):
        if self.debug <= 0:
            return

        if debug and self.debug < debug:
            return

        if not isinstance(message, six.string_types):
            message = str(message)

        click.secho(message, **style)

    def error(self, *args, **kwargs):
        kwargs['bold'] = True
        kwargs['fg'] = 'red'
        self(*args, **kwargs)

    def warning(self, *args, **kwargs):
        kwargs['bold'] = True
        kwargs['fg'] = 'yellow'
        self(*args, **kwargs)

    def info(self, *args, **kwargs):
        kwargs['bold'] = False
        kwargs['fg'] = 'blue'
        self(*args, **kwargs)

    def success(self, *args, **kwargs):
        kwargs['bold'] = False
        kwargs['fg'] = 'green'
        self(*args, **kwargs)


class ConfigSection(object):
    def __init__(self, config, section):
        self._config = config
        self._section = section

    def __getattr__(self, k):
        if k.startswith('_'):
            return self.__getattribute__(k)
        return self._config._data[self._section].get(k)

    def __setattr__(self, k, v):
        if k.startswith('_'):
            object.__setattr__(self, k, v)
        else:
            self._config._data[self._section][k] = v

    def __delattr__(self, k):
        if k in self._config._data[self._section]:
            del self._config._data[self._section][k]


class Config(object):

    def __init__(self, filename):
        self.filename = filename
        self._data = {}
        self.config = SafeConfigParser()
        self.config.read(filename)

    def set(self, section, key, value):
        if section not in self.config.sections():
            self.create_section(section)
        self.config.set(section, key, value)
        return self

    def get(self, section, key):
        try:
            return self.config.get(section, key)
        except NoOptionError:
            return None
        except NoSectionError:
            return None

    def create_section(self, section):
        self.config.add_section(section)

    def save(self):
        with open(self.filename, 'wb') as configfile:
            self.config.write(configfile)


class Context(object):
    def __init__(self, config_filename, debug):
        config_filename = config_filename or settings.CONFIG_DEFAULT_PATH

        self.config = Config(config_filename)
        self.echo = Echo(debug)
        self.model = None

        # utils.set_loglevel(40)

        # MachinePackViewer - required in most cases
        # sys.path.insert(0, os.path.abspath(os.path.curdir))

        self.machinepack_viewer = MachinePackViewer()
        self.machinepack_viewer.echo = self.echo
