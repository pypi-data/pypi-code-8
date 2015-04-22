import click

from sascar_client.soap_client import Vehicles


@click.command('sascar_client')
@click.option('--get_vehicles', is_flag=True,
    help='Save vehicles to the database.')
@click.option('--host', default='localhost',
    help='Set URL of the database server. Default value is localhost.')
@click.option('--port', default=5432,
    help='Set port of database server. Default value is 5432.')
@click.option('--hours', default=24,
    help='Set the number of prior hours you want to query. Default value is 24')
@click.argument('user', type=str, metavar='<user>')
@click.argument('password', type=str, metavar='<password>')
@click.argument('database', type=str, metavar='<database>')
@click.argument('dbuser', type=str, metavar='<dbuser>')
@click.argument('dbpassword', type=str, metavar='<dbpassword>')
def cli(get_vehicles, user, password, database, dbuser, dbpassword, host, port, hours):
    """Get the routes of all vehicles and save it to a database.
    User and password fields refer to your sascar user and password."""
    connection = Vehicles(user, password, database, dbuser, dbpassword, host, port)
    if get_vehicles:
        connection.save_vehicles()
    connection.save_routes(hours)
    connection.close_dbcon()
