import click

from ..decorators import machinepack_required


@click.command()
@click.pass_obj
@click.option('--name', prompt='=Machine name', help='Name of the machine you want to copy')
@click.option('--newname', prompt='New machine name', help='Name of the machine you want to create')
@machinepack_required
def cli(ctx):
    """ copy machine """
    pass
