import subprocess
import click

from machinepack.decorators import machinepack_required
from machinepack.helpers import next_version


@click.command()
@click.pass_obj
# @click.option('--version', help='Version of machinepack', prompt='Machinepack version', default='0.2')
@machinepack_required
def cli(ctx):
    """ get pack metadata """

    # TODO: write better new version


    version_str = ctx.machinepack_viewer.package_config['version']
    next_version_str = next_version(version_str)

    value = click.prompt('Next version number (current: %s)' % version_str, default=next_version_str)

    subprocess.call('python setup.py register -r pypitest', shell=True)
    subprocess.call('python setup.py sdist upload -r pypitest', shell=True)


