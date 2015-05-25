from datetime import datetime

from open_weather_forecast.info_extractor.get_info import GetInfo
from open_weather_forecast.info_extractor.forecast.forecast_weather_info import Base, ForecastWeather, Temperature
from open_weather_forecast.conf.constants import WEATHER_DATE_FORMAT


class GetForecast(GetInfo):

    def __init__(self):
        super(GetForecast).__init__()
        self.engine = None
        self.password = None
        self.username = None
        self.host = None
        self.db_name = None
        self.db_url = None
        self.base = Base
        self.session = None

    def store_data(self, data):
        self.get_db_connection()
        self.get_db_session()
        for point in data:
            existing_weather = self.session.query(ForecastWeather).filter_by(dt_txt=point.get("dt_txt")).first()
            if not existing_weather:
                # Create
                new_temperature = Temperature(**point.get("main"))
                self.session.add(new_temperature)
                weather_pk = datetime.strptime(point.get("dt_txt"), WEATHER_DATE_FORMAT)
                new_weather_point = ForecastWeather(dt_txt=weather_pk, temperature=new_temperature)
                self.session.add(new_weather_point)

        self.session.commit()

    def load_data(self):
        self.get_db_connection()
        self.get_db_session()
        res = {list(x.serialize.keys())[0]: x.serialize.get(list(x.serialize.keys())[0]) for x in self.session.query(ForecastWeather).all()}
        self.session.close()
        return res


