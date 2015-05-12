import click

from . import utils
from . import settings
from .context import Context
from machinepack.print_helpers import print_version


@click.group(cls=utils.AutodiscoverMultiCommand, context_settings=settings.CONTEXT)
@click.option('--config', '-c', type=click.Path(exists=True, file_okay=True, readable=True), default=None)
@click.option('--version', '-v', is_flag=True, callback=print_version, expose_value=False, is_eager=True)
@click.option('--debug', '-d', count=True, default=1)
@click.pass_context
def cli(ctx, config, debug):
    ctx.obj = Context(config, debug)
