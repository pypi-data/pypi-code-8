import click

from fixturegen.exc import NoSuchTable, WrongDSN
from fixturegen.generator import generate, sqlalchemy_data

@click.command()
@click.argument('dsn', required=True)
@click.argument('table', required=True)
@click.option('--limit')
@click.option('--where')
@click.option('--order-by')
def sqlalchemy(dsn, table, limit=None, where=None, order_by=None):
    try:
        click.echo(generate(*sqlalchemy_data(table, dsn, limit, where, order_by)))
    except NoSuchTable:
        click.echo('No such table', err=True)
    except WrongDSN:
        click.echo('Wrong DSN', err=True)
