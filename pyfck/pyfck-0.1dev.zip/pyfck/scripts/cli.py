import click

import pyfck


@click.command('pyfck')
@click.argument('filename', default="main.bf", type=str)
@click.option('--direct', default=None, type=str)
def cli(filename, direct):
    # TODO: Flesh this description out
    """
    Runs the damn program
    :param count:
    :return:
    """
    if direct is not None:
        interpreter = pyfck.Interpreter(direct_input=direct)
    else:
        interpreter = pyfck.Interpreter(filename=filename)

    interpreter._run()
