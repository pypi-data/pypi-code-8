import click

from machinepack.decorators import machinepack_required
from machinepack.helpers import cmd_print_machines


@click.command()
@click.option('--name', help='Name of the machine')
@click.pass_obj
@machinepack_required
def cli(ctx, name):
    """ run machine """

    if not name:
        cmd_print_machines(ctx, full=False)
        name = click.prompt("Machine name", type=click.Choice(ctx.machinepack_viewer.machines_list), default='all')

    if name == 'all':
        machines_list = ctx.machinepack_viewer.machines_list
    else:
        machines_list = [name]

    for machine_name in machines_list:
        ctx.machinepack_viewer.exec_machine(machine_name)
