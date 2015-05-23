from sqlalchemy import create_engine

password = ""
username = ""
db_url = 'postgresql+pg8000://{}:{}@yeraydbinstances.crzn8kwn8uzj.us-east-1.rds.amazonaws.com/openweatherdata'.format(username, password)

engine = create_engine()
engine.connect()

