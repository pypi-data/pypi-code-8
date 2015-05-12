# -*- coding: utf-8 -*-

import click
from pygments import highlight
from pygments.lexers.python import PythonLexer
from pygments.formatters.terminal256 import Terminal256Formatter

from machinepack import __version__


# TODO: move template to templates
BANNER_TEMPLATE = r"""
   ______
  /      \      machinepack (CLI Tool)
 /  |  |  \     v0.1
 \        /
  \______/      http://python-machine.org
"""


def print_machines_list(machines_list, machine_class):
    for module in machines_list:
        click.secho("    • %s.%s()" % (machine_class, module), fg='cyan')
    click.echo()


def print_banner():
    click.secho(BANNER_TEMPLATE, fg='cyan')


def print_error(msg):
    click.secho(msg, fg='red')


def print_python_code(code):
    click.echo(highlight(code, PythonLexer(), Terminal256Formatter()))


def print_version(ctx, param, value):
    if not value or ctx.resilient_parsing:
        return
    click.echo(__version__)
    ctx.exit()
