# -*- coding: utf-8 -*-

import os
import itertools

import click
from distutils.version import LooseVersion
from mako.template import Template
from colorama import Style
from colorama import init

init(autoreset=True)


def render(file_name, args):
    params = {
        'Style': Style,
    }
    params.update(args)

    template_file = os.path.join(os.path.dirname(__file__), 'templates/%s.mako' % file_name)
    return Template(filename=template_file).render(**params)


def cmd_print_machines(ctx, full=True):
    click.echo()
    click.secho("There are ", nl=False)
    click.secho("%s" % len(ctx.machinepack_viewer.machines_list), nl=False, fg='cyan')
    click.secho(" machines in this machinepack:")
    click.secho("=========================================")

    for module in ctx.machinepack_viewer.machines_list:
        if full:
            click.secho("    ○ %s.%s()" % (ctx.machinepack_viewer.machine_class, module), fg='cyan')
        else:
            click.secho("    ○ %s" % module, fg='cyan')
    click.echo()

def next_version(current_version_str):
    version = LooseVersion(current_version_str).version
    return ".".join([str(x) for x in tuple(itertools.chain(version[0:-1], [version[-1] + 1]))])
