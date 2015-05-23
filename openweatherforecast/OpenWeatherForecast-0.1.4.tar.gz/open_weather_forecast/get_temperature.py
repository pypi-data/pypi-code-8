from open_weather_forecast.get_info import GetInfo
from open_weather_forecast.db_connection import get_db_connection


class GetTemperature(GetInfo):

    def __init__(self):
        super(GetTemperature).__init__()
        self.db = None

    def store_data(self):
        self.db = get_db_connection()
        import ipdb
        ipdb.set_trace()
