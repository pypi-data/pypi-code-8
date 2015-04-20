__author__ = 'hvishwanath'


from peewee import *
from ..settings import *

import datetime

DB = SqliteDatabase(dbfile, threadlocals=True)

class BaseModel(Model):
    class Meta:
        database = DB

class Provider(BaseModel):
    providername = CharField(unique=True)
    username = CharField()
    password = CharField()

class Application(BaseModel):
    appid = CharField(unique=True)
    giturl = CharField()
    weburl = CharField()
    provider = ForeignKeyField(Provider, related_name='provider')

    def __repr__(self):
        return self.__str__()

    def __str__(self):
        msg = """
        AppID: %s
            git_url: %s
            weburl: %s
            platform: %s
        """
        return msg % (self.appid, self.giturl, self.weburl, self.provider.providername)


def db_init():
    DB.connect()
    DB.create_tables([Application, Provider], safe=True)

def db_reset():
    os.remove(dbfile)
    DB.connect()
    DB.create_tables([Application, Provider], safe=True)
