# -*- coding: utf-8 -*-

import os

import click

import machinepack


CONTEXT = {
    'auto_envvar_prefix': 'MACHINEPACK',
}

LOGLEVELS = [
    'ERROR',
    'WARNING',
    'INFO',
    'DEBUG',
    'NOTSET',
]

COMMANDS_FOLDER = os.path.abspath(
    os.path.join(os.path.dirname(__file__), 'commands')
)

CONFIG_FILENAME = '.machinepack'
CONFIG_DIR_SETTINGS = {
    'app_name': machinepack.__title__,
    'roaming': True,
    'force_posix': True
}
CONFIG_DEFAULT_PATH = click.get_app_dir(**CONFIG_DIR_SETTINGS)

ALIASES = {
    # 'login': 'auth.login',
    # 'logout': 'auth.logout',
}
