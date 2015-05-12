import sys

import click

from ..decorators import machinepack_required
from ..print_helpers import print_python_code
from ..helpers import cmd_print_machines


@click.command()
@click.option('--name', help='Name of the machine')
@click.pass_obj
@machinepack_required
def cli(ctx, name):
    """ machine usage example """

    if not name:
        cmd_print_machines(ctx, full=False)
        name = click.prompt("Machine name", type=click.Choice(ctx.machinepack_viewer.machines_list), default=ctx.machinepack_viewer.machines_list[0])

    code = ctx.machinepack_viewer.generate_example(name)

    if code:
        print_python_code(code)
    else:
        sys.exit(1)
