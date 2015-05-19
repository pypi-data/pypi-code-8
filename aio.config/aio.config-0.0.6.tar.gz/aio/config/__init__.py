import os
import asyncio

from configparser import ConfigParser, ExtendedInterpolation

from aio.core.exceptions import MissingConfiguration


def find_config(app_dir=None):
    if not app_dir:
        app_dir = os.getcwd()
    config = os.path.join(app_dir, 'aio.conf')
    if os.path.exists(config):
        return config
    config = os.path.join(app_dir, 'etc', 'aio.conf')
    if os.path.exists(config):
        return config
    config = os.path.join(app_dir, '/etc', 'aio.conf')
    if os.path.exists(config):
        return config
    raise MissingConfiguration('no configuration file found')


@asyncio.coroutine
def parse_config(config=None, app_dir=None, config_dict=None, config_string=None):
    parser = ConfigParser(interpolation=ExtendedInterpolation())
    if config_dict:
        parser.read_dict(config_dict)
    elif config_string:
        parser.read_string(config_string)
    else:
        parser.read_file(open(config or find_config(app_dir)))
    return parser
