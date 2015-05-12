import click

from ..decorators import machinepack_required
from ..helpers import cmd_print_machines


@click.command()
@click.pass_obj
@click.option('--name', help='Name of the machine', type=click.STRING)
@machinepack_required
def cli(ctx, name):
    """ run machine tests """

    if not name:
        cmd_print_machines(ctx, full=False)
        name = click.prompt("Machine name", type=click.Choice(ctx.machinepack_viewer.machines_list), default='all')

    if name == 'all':
        name = None

    ctx.machinepack_viewer.make_tests(name)

