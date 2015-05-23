import os
import configparser

from climb.exceptions import ConfigNotFound

DEFAULT_CONFIG_PATHS = [
    './{name}.conf',
    '~/.{name}.conf',
    '/etc/{name}/{name}.conf',
]


def load_config(name):
    config = configparser.ConfigParser()

    paths = [path.format(name=name) for path in DEFAULT_CONFIG_PATHS]
    for config_path in paths:
        config_path = os.path.expanduser(config_path)
        if os.path.isfile(config_path) and os.access(config_path, os.R_OK):
            config.read(config_path)
            break
    else:
        raise ConfigNotFound("Could not find {name}.conf".format(name))

    return config
