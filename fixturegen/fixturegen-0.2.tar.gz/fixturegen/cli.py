import click

from fixturegen.exc import NoSuchTable, WrongDSN
from fixturegen.generator import generate, sqlalchemy_data

@click.command()
@click.option('--table')
@click.option('--dsn')
@click.option('--limit')
@click.option('--where')
@click.option('--order-by')
def sqlalchemy(table, dsn, limit=None, where=None, order_by=None):
    try:
        click.echo(generate(*sqlalchemy_data(table, dsn, limit, where, order_by)))
    except NoSuchTable:
        click.echo('No such table', err=True)
    except WrongDSN:
        click.echo('Wrong DSN', err=True)
