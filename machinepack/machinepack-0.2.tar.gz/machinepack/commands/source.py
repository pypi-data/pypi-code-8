import click

from machinepack.decorators import machinepack_required
from machinepack.print_helpers import print_python_code


@click.command()
@click.pass_obj
@click.option('--name', help='Name of the machine', prompt='Machine name')
@machinepack_required
def cli(ctx, name):
    """ print machine source """

    code = ctx.machinepack_viewer.get_source(name)
    print_python_code(code)


