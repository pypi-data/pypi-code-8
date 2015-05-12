import subprocess

import click

from machinepack.decorators import machinepack_required
from machinepack.helpers import next_version


@click.command()
@click.pass_obj
@machinepack_required
def cli(ctx):
    """ upload new version of machinepack to PyPi """

    version_str = ctx.machinepack_viewer.package_config['version']
    next_version_str = next_version(version_str)

    # TODO: update version in version file
    value = click.prompt('Next version number (current: %s)' % version_str, default=next_version_str)

    subprocess.call('python setup.py sdist upload -r pypitest', shell=True)
