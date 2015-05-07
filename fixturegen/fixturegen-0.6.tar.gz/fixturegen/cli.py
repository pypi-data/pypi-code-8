import click

from fixturegen.exc import NoSuchTable, WrongDSN
from fixturegen.generator import generate, sqlalchemy_data


@click.command()
@click.argument('dsn', required=True)
@click.argument('table', required=True)
@click.option('--limit', help='Limit fixture count', type=click.INT)
@click.option('--where', help='Filter result. i.e. "id > 2"')
@click.option('--order-by', help='Order fixture output. i.e. "id DESC"')
@click.option('--with-import/--without-import', help='Add import statement',
              default=True)
@click.option('--fixture-class-name', help='Set fixture class name')
@click.option('--naming-row-columns', help="""Columns that identifies
                                              class name
                                              for each row in fixture.
                                              Specify multiple columns
                                              by commas""")
def sqlalchemy(dsn, table, limit=None, where=None,
               order_by=None, with_import=True, fixture_class_name=None,
               naming_row_columns=None):
    """
    Provide DSN and Table name for fixture generation
    """
    if naming_row_columns:
        naming_columns = naming_row_columns.split(',')
    else:
        naming_columns = None

    try:
        click.echo(generate(
            *sqlalchemy_data(table, dsn, limit, where, order_by),
            with_import=with_import, fixture_class_name=fixture_class_name,
            row_naming_columns=naming_columns),
        )
    except NoSuchTable:
        click.echo('No such table', err=True)
    except WrongDSN:
        click.echo('Wrong DSN', err=True)
