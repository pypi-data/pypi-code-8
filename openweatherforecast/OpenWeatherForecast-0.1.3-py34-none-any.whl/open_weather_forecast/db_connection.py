from sqlalchemy import create_engine

from open_weather_forecast.conf.global_settings import get_global_settings


gs = get_global_settings()
password = gs["password"]
username = gs["username"]
host = gs["host"]
db_name = gs["db_name"]

db_url = 'postgresql+pg8000://{username}:{password}@{host}/{db_name}'.format(
    username=username,
    password=password,
    host=host,
    db_name=db_name
)

engine = create_engine()
engine.connect()

