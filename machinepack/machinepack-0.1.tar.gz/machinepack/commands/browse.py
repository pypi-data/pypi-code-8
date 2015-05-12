import subprocess

import click

from machinepack.decorators import machinepack_required


@click.command()
@click.pass_obj
@machinepack_required
def cli(ctx):
    """ view on python-machine.org """

    subprocess.call(['open', ctx.machinepack_viewer.package_config['url']])
