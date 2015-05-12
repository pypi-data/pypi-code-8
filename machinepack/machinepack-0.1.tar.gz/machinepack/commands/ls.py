import click

from machinepack.decorators import machinepack_required
from machinepack.helpers import cmd_print_machines


@click.command()
@click.pass_obj
@machinepack_required
def cli(ctx):
    """ list machines """

    cmd_print_machines(ctx)
