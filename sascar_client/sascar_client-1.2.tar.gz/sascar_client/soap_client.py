from __future__ import print_function

from suds.client import Client
from shapely.geometry import Point

from datetime import datetime, timedelta

from .database import Database


def record(position, date, last_position, last_date):
    """Compare two positions and define if it needs to be recorded in the
    database or not. To be recorded the distance needs to be greater than
    0.004 and the time diference needs to be greater than 3 min."""

    time_diff = date - last_date
    distance = Point(position).distance(Point(last_position))

    if distance >= 0.004 and time_diff > timedelta(minutes=3):
        return True
    else:
        return False


class Vehicles(object):
    """
    A class to connect to sascar soap, get the data and save in a database.
    """

    def __init__(self, user, password, dbname, dbuser, dbpassword,
                    host='localhost', port='5432'):

        self.url = 'http://sasintegra.sascar.com.br/SasIntegra/SasIntegraWSService?wsdl'
        self.client = Client(self.url)
        self.user = user
        self.password = password
        self.dbcon = Database(dbname, dbuser, dbpassword, host, port)

    def get_vehicles(self):
        """Return a list of vehicles with its id and plate."""

        vehicles = self.client.service.obterVeiculos(self.user, self.password,
            1000)
        return [[car.idVeiculo, car.placa] for car in vehicles]

    def save_vehicles(self):
        """Save the id and plate of vehicles in the database."""

        data = self.get_vehicles()
        for id, plate in data:
            self.dbcon.add_vehicle(id, plate)

    def save_routes(self, hours=24):
        """
        Get the routes of the last 24 hours of all vehicles and save it in the
        database. The number of prior hours to query can be defined in the
        parameter 'hours'.
        """

        now = datetime.now()
        start_date = now - timedelta(hours=hours)
        vehicles = self.get_vehicles()

        for id, plate in vehicles:
            route = self.client.service.obterPacotePosicaoHistorico(
                self.user,
                self.password,
                start_date.strftime('%d/%m/%Y %H:%M'),
                now.strftime('%d/%m/%Y %H:%M'),
                id
                )

            if len(route) > 0:
                # just to initialize the variables with a valid value
                last_date = now - timedelta(2)
                last_position = (0, 0)

                for status in route:
                    if status.ignicao == 1:
                        turned_on = True
                    else:
                        turned_on = False

                    position = (status.latitude, status.longitude)
                    if record(position, status.dataPacote, last_position,
                                last_date):
                        self.dbcon.add_status(
                            status.idVeiculo,
                            status.longitude,
                            status.latitude,
                            status.dataPacote,
                            status.velocidade,
                            turned_on
                            )
                        last_position = (status.latitude, status.longitude)
                        last_date = status.dataPacote

    def close_dbcon(self):
        """Close database connection"""
        self.dbcon.close()
