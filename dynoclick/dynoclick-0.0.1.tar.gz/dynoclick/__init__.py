import click
import importlib


class DynoCli(click.MultiCommand):

    def __init__(self, modules, *args, **kwargs):
        self.modules = modules
        return super(DynoCli, self).__init__(*args, **kwargs)

    def list_commands(self, ctx):
        return sorted(self.modules)

    def get_command(self, ctx, name):
        try:
            module = importlib.import_module("{module}.cli".format(module=name))
        except ImportError:
            raise ImportError("Could not find CLI module for %s" % name)
        if not hasattr(module, 'cli'):
            raise ImportError("{module}.cli does not have `cli` object".format(module=name))
        return module.cli

