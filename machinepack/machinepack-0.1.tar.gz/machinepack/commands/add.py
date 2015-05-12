import click


@click.command()
@click.pass_obj
@click.option('--name', help='Name of the machine')
def cli(ctx, name):
    """ add machine """

    ctx.machinepack_viewer.generate_machine(name)