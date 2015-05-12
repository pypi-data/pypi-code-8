import subprocess

import click

from ..decorators import machinepack_required


@click.command()
@click.pass_obj
@machinepack_required
def cli(ctx):
    """ get pack metadata """

    subprocess.call('python setup.py register -r pypitest', shell=True)

