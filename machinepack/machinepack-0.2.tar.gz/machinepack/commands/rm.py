import click

from machinepack.decorators import machinepack_required


@click.command()
@click.pass_obj
@click.option('--name', prompt='Machine name', help='Name of the machine you want to copy', confirmation_prompt=True)
@machinepack_required
def cli(ctx, name):
    """ delete existing machine """
    pass

