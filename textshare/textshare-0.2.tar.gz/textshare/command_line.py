import click, textshare, os

@click.command()
@click.option('-f', '--file', type=click.Path(exists=True), help='filename to be shared', nargs=1, required=True)
def cli(file):
    click.echo(textshare.uploadfile(file))
