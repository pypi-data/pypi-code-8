import click

from ..decorators import machinepack_required


@click.command()
@click.pass_obj
@machinepack_required
def cli(ctx):
    """ rename machine """
    pass
