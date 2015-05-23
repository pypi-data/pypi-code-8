from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, Float

Base = declarative_base()


class ForecastWeatherInfo(Base):
    __tablename__ = 'forecast_weather_info'
    dt_txt = Column(String, primary_key=True, autoincrement=False)


