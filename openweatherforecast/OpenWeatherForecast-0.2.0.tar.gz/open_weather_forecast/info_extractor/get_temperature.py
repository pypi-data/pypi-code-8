from datetime import datetime

from open_weather_forecast.info_extractor.get_info import GetInfo
from open_weather_forecast.weather_db.weather_info import Base, WeatherInfo, Temperature


class GetTemperature(GetInfo):

    def __init__(self):
        super(GetTemperature).__init__()
        self.engine = None
        self.password = None
        self.username = None
        self.host = None
        self.db_name = None
        self.db_url = None
        self.base = Base
        self.session = None

    def download_store_new_data(self, url="", information_schema=None):
        error, info_filtered_by_schema = self.get_info(url=url, information_schema=information_schema)
        if not error:
            self.store_data(info_filtered_by_schema.get("list"))
        else:
            msg = "An error occurred while downloading new data"
            raise Exception(msg)

    def store_data(self, data):
        self.get_db_connection()
        self.get_db_session()
        for point in data:
            existing_weather = self.session.query(WeatherInfo).filter_by(dt_txt=point.get("dt_txt")).first()
            if not existing_weather:
                # Create
                new_temperature = Temperature(**point.get("main"))
                self.session.add(new_temperature)
                weather_pk = datetime.strptime(point.get("dt_txt"), "%Y-%m-%d %H:%M:%S")
                new_weather_point = WeatherInfo(dt_txt=weather_pk, temperature=new_temperature)
                self.session.add(new_weather_point)

        self.session.commit()

    def load_data(self):
        self.get_db_connection()
        self.get_db_session()

        return [x.serialize for x in self.session.query(WeatherInfo).all()]


