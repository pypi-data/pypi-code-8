import os
import asyncio
from collections import OrderedDict
from configparser import ConfigParser, ExtendedInterpolation

# from aio.core.exceptions import MissingConfiguration


def gather_config(modules, filename=None):
    config_files = []
    for module in modules:
        path = module.__path__[0]
        app_config = os.path.join(path, filename or "aio.conf")
        if os.path.exists(app_config):
            config_files.append(app_config)
    return config_files


def find_config(app_dir=None, filename=None, system_folder=None):
    if not app_dir:
        app_dir = os.getcwd()
    config = os.path.join(app_dir, filename or 'aio.conf')
    if os.path.exists(config):
        return config
    config = os.path.join(app_dir, 'etc', filename or 'aio.conf')
    if os.path.exists(config):
        return config
    if not system_folder:
        system_folder = os.path.join("/etc", "aio")
    config = os.path.join(system_folder, filename or 'aio.conf')
    if os.path.exists(config):
        return config


def parse_config(config=None, config_files=None, app_dir=None,
                 config_dict=None, config_string=None,
                 modules=None, parser=None, interpolation=None,
                 filename=None, search_for_config=False):
    parser = parser or ConfigParser(
        interpolation=interpolation or ExtendedInterpolation())
    if config_dict:
        parser.read_dict(config_dict)
    elif config_string:
        parser.read_string(config_string)
    elif config_files:
        for config_file in config_files:
            parser.read_file(open(config))
    elif modules:
        for config_file in gather_config(modules, filename=filename):
            parser.read_file(open(config_file))
    elif config or search_for_config:
        config = config or find_config(app_dir, filename=filename)
        if config:
            parser.read_file(open(config))
    return parser


class ConfigSection(OrderedDict):

    pass


class Config(OrderedDict):

    pass


def replicate_config(config, test_section=None):
    new_config = Config()
    for section_name, section in config.items():
        if test_section:
            if not test_section(section_name):
                continue
        new_config[section_name] = ConfigSection()
        for option_name, option in section.items():
            new_config[section_name][option_name] = option
    return new_config


def dump_config(config):
    for section_name, section in config.items():
        print("[%s]" % section_name)
        for option_name, option in section.items():
            print("%s = %s" % (option_name, str(option.replace("\n", "\n\t"))))
        print()
