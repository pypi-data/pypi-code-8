from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy import Column, Integer, Float, ForeignKey, DateTime

Base = declarative_base()


class Temperature(Base):
    __tablename__ = 'temperature'
    id = Column(Integer, primary_key=True, autoincrement=True)
    temp_max = Column(Float, nullable=False)
    temp_min = Column(Float, nullable=False)
    temp = Column(Float, nullable=False)


class WeatherInfo(Base):
    __tablename__ = 'weatherinfo'
    dt_txt = Column(DateTime, primary_key=True, autoincrement=False)
    temperature_id = Column(Integer, ForeignKey('temperature.id'))
    temperature = relationship(Temperature)

    @property
    def serialize(self):
        """Return object data in easily serializeable format"""
        return {self.dt_txt: {
            "temp_max": self.temperature.temp_max,
            "temp_min": self.temperature.temp_min,
            "temp": self.temperature.temp,
            }}
