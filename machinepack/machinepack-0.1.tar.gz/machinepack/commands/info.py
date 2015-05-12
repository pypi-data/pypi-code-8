import click

from ..print_helpers import print_machines_list
from ..decorators import machinepack_required


@click.command()
@click.pass_obj
@machinepack_required
def cli(ctx):
    """ get pack metadata """

    package_config = ctx.machinepack_viewer.package_config

    click.echo()
    click.echo()
    click.secho(package_config['name'], nl=False, bold=True)
    click.echo(" -- " + package_config['description'])
    click.echo()
    click.echo()
    click.secho("URLS", bold=True)
    click.echo('   ' + package_config['url'])
    click.echo()
    click.echo()

    click.secho("INSTALLATION", bold=True)
    click.echo('   pip install %s' % package_config['name'])
    click.echo()
    click.echo()

    click.secho("USAGE", bold=True)
    click.echo('   from %s import %s' % (package_config['name'], package_config['name'].split('_')[1].title()))
    click.echo()
    click.echo()

    click.secho("AVAILABLE METHODS", bold=True)
    print_machines_list(ctx.machinepack_viewer.machines_list, ctx.machinepack_viewer.machine_class)
    click.echo()
    click.echo()




