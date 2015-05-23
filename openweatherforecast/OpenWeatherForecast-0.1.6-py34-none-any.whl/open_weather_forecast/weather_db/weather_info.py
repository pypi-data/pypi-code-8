from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, Float

Base = declarative_base()


class WeatherInfo(Base):
    __tablename__ = 'weather_info'
    dt_txt = Column(String, primary_key=True, autoincrement=False)


class Temperatures(Base):
    __tablename__ = 'temperatures'
    id = Column(Integer, primary_key=True, autoincrement=True)
    max = Column(Float, nullable=False)
    min = Column(Float, nullable=False)
    average = Column(Float, nullable=False)
