import yama
import click
import subprocess


@click.group()
def cli():
    pass


@cli.command()
def audit():
    """
    Audit running processes to check for expected processes.
    """
    yama.audit()


@cli.command()
@click.argument('cmd', nargs=-1)
def run(cmd):
    """
    Run any command, with yama monitoring.
    """
    proc = subprocess.Popen(cmd)
    pid = proc.pid
    yama.register(pid)
    try:
        proc.wait()
    except KeyboardInterrupt:
        pass
    finally:
        yama.deregister(pid)
