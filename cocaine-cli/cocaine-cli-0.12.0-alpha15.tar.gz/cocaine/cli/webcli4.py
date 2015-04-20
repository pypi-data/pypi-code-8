

import json
import collections
import click
import getpass
from os.path import expanduser, join, isfile
import os
import re
import sys

from pprint import pprint

import collections

import requests

from config_reader import ProjectReader, VersionReader

from cocaine.cli.util import make_archive

try:
    from io import BytesIO  # py3
except ImportError:
    from cStringIO import StringIO as BytesIO  # py2

import logging
log = logging.getLogger()
log.setLevel(logging.INFO)

from .client import *

class MyGroup(click.Group):

    def __init__(self, commands=None, **kwargs):
        super(MyGroup, self).__init__(commands=commands, **kwargs)

        self.commands = commands or collections.OrderedDict()
    
    def list_commands(self, ctx):
        return list(self.commands)

b = ""
def blank():
    global b
    b += " "
    return b




@click.group(cls=MyGroup)
@click.pass_context
@click.option('sets', '--set', nargs=2, multiple=True, required=False,
              metavar="<k.e.y> <val>",
              help="override or provide corresponding fields of ./project.json")
@click.option('--no-config', "--nc", is_flag=True,
              help="don't load ./project.json (to manage projects other than current)")
@click.option('--save', is_flag=True,
              help="store --set fields to ./project.json")
@click.option('--debug', is_flag=True,
              help="spew more logs")
def cli(ctx, debug, nc, sets, save):
    """DON'T PANIC.

    Deliver your project to the public cloud with steps listed below
    in the Commands section.

    Or take your time and get acquainted with their --help messages.
    """
    pass


@cli.command(short_help="set and verify a cloud API entry point and an auth token")
@click.option('--url', required=True, metavar="URL", help="API server base url")
@click.option('--token', metavar="AUTH_TOKEN", type=click.STRING)
def login(ctx):
    "set and verify a cloud API entry point and an auth token"
    pass

@cli.group(cls=MyGroup, name=blank())
def _separator(ctx):
    pass


@cli.group(cls=MyGroup,
           short_help=
           """initialize a new ./project.json file with defaults and blanks
           please, 8<---- tweak generated project.json to suit to your needs
           """)
def init():

    pass

@cli.group(cls=MyGroup, name=blank())
def _separator():
    pass

@cli.command(cls=MyGroup, short_help="create a new cloud project described in ./project.json")
@click.option('--force', '-f', is_flag=True,
              help="force an update of the existing project")
def create(force, **kwargs):
    "create a new project in a cloud described in ./project.json"

    pass

@cli.group(cls=MyGroup, name=blank())
def _separator(ctx):
    pass


@cli.command(short_help="push an app version to the cloud, then build it")
@click.option('--force', '-f', is_flag=True,
              help="force an update of the existing version")
@click.option('--no-build', '-n', is_flag=True,
              help="don't schedule build of a container")
@click.option('--no-docker', is_flag=True,
              help="don't use docker conteinerization")
@click.option('--increment', '-i', is_flag=True,
              help="increment version in package.json")
@click.option('--version', '-v', help="set version in package.json")
def push(force, no_build, no_docker, increment,  version, **kwargs):
    "push an app version to the cloud, then build it"

    pass


@cli.command(short_help="deploy an alredy built version to the <target> cluster")
@click.option('-u', is_flag=True,
              help="undeploy version from cluster")
@click.argument("target", metavar="<target>")
def deploy(target, u, **kwargs):
    "deploy an alredy built version to the <target> cluster"

    pass

@cli.command(short_help="balance a load between versions at the <target> cluster")
@click.argument("target", metavar="<target>")
def balance(target, **kwargs):
    """
    balance load between versions at the <target> cluster

    looks up routing info in your project.json, updates
    cluster configuration for the project, and performs
    a corresponding balance task.
    """
    pass


@cli.command(name="deliver", short_help="perform all three of the above steps with one command")
@click.option('--increment', '-i', is_flag=True,
              help="increment version in package.json")
@click.option('--version', '-v', help="set version in package.json")
@click.option('--no-docker', is_flag=True,
              help="don't use docker conteinerization")
@click.argument("target", metavar="<target>")
def deliver(increment,  version, no_docker, target, **kwargs):
    """
    perform all three of the above steps with one command

    pushes, deploys to <target> cluster and configures routing
    with one route, pointing to version it pushed with weight of 10
    """

    pass

@cli.group(cls=MyGroup, name=blank())
def _separator(ctx):
    pass

@cli.group(cls=MyGroup)
def show(ctx):
    "inspect various minutae and statuses"
    pass

@cli.group(cls=MyGroup, name=blank())
def _separator(ctx):
    pass


@cli.group(cls=MyGroup)
def task(ctx):
    "tasks-related subcommands"
    pass

@task.command()
@click.argument("task-id")
def status(task_id):
    "display status for given task-id"

    pass

@task.command()
@click.argument("task-id")
def retry(task_id):
    "retry task with task-id"
    pass


@cli.group(cls=MyGroup)
def project(ctx):
    "manage project configuration"
    pass

@cli.group(cls=MyGroup)
def version(ctx):
    "manage version configuration"
    pass

@cli.group(name=blank())
def _separator():
    pass
    
@cli.group(name=blank(), short_help="have to be a platform admin to do this:")
def _separator():
    pass
    
@cli.group(cls=MyGroup, short_help="manage cloud clusters")
def cluster(ctx):
    "manage cloud clusters (you have to be a platform admin to do this)"
    pass

@cli.group(cls=MyGroup, short_help="manage global users")
def user(ctx):
    "manage global users"
    pass

@cli.group(cls=MyGroup, name=blank())
def _separator(ctx):
    pass
    

