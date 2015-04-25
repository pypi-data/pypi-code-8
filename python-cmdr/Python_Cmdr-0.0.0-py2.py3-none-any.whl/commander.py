#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import absolute_import

import click

from .config import config


# Treat commands as plugins with the help of `pluginbase` library
from pluginbase import PluginBase
plugin_base = PluginBase(package='cmdr.commands')
plugin_source = plugin_base.make_plugin_source(searchpath=[config.COMMANDS_PATH])


class Commander(object):
    def __init__(self, name):
        self.name = name
        for command_name in plugin_source.list_plugins():
            if command_name == name:
                self.job = plugin_source.load_plugin(command_name)
                break
        else:
            raise RuntimeError(
                'Command `{0}` not found. Please ensure that a Python '
                'module (or package) named "{0}.py" (or "{0}/__init__.py") '
                'exists in "{1}"'.format(name, config.COMMANDS_PATH)
            )

    def execute(self, *args):
        try:
            entry_point = getattr(self.job, config.ENTRY_POINT)
        except AttributeError:
            raise RuntimeError(
                'Entry point `{0}` not found. Please ensure that a '
                'function named "{0}" exists in the Python module '
                '(or package) "{1}.py" (or "{1}/__init__.py") '.format(
                    config.ENTRY_POINT, self.name
                )
            )
        entry_point(*args)


@click.command()
@click.argument('command_name')
@click.argument('args', nargs=-1)
def main(command_name, args):
    commander = Commander(command_name)
    commander.execute(*args)


if __name__ == '__main__':
    main()
