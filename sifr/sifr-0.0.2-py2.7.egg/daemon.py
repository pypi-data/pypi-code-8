import anyconfig
import click


class SifrD(object):
    def __init__(self, debug=False):
        self.debug = debug

class AnyConfigType(click.File):
    name = 'config'

    def convert(self, value, param, ctx):
        fp = super(AnyConfigType, self).convert(value, param, ctx)
        try:
            config = anyconfig.load(fp.name)
            if not config:
                raise ValueError
            return config
        except ValueError:
            self.fail(
                'Could not load configuration from file: %s.'
                'It must be one of yaml/ini/json' % (fp.name)
            )

@click.group()
@click.option('--debug/--no-debug', default=False)
@click.pass_context
def cli(ctx, debug):
    ctx.obj = SifrD(debug)


if __name__ == "__main__":
    cli(auto_envvar_prefix='SIFR')
