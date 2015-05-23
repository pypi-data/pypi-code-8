import requests
from requests import RequestException
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from functools import wraps

from open_weather_forecast.info_extractor.http_decorator import auto_tries
from open_weather_forecast.info_extractor.get_info_abstract import GetInfoAbstract
from open_weather_forecast.conf.global_settings import get_global_settings


class GetInfo(GetInfoAbstract):

    def __del__(self):
        if hasattr(self, "session") and self.session:
            self.session.close()

    def filter_information(self, info_retrieved, schema, result=None):
        """
        :param info_retrieved: Info retrieved from the API
        :param schema: Schema defined by the user to extract partial information
        :param result: Structure containing the filtered information from the API
        :return:
        """
        if result is None:
            result = dict()

        for key in schema:
            if isinstance(info_retrieved, dict):
                value = info_retrieved.get(key, {})
            else:
                for element, sub_info in zip(info_retrieved, schema*len(info_retrieved)):
                    result.append(type(element)())
                    self.filter_information(element, sub_info, result[-1])
                continue

            info_type = type(schema.get(key)) if isinstance(schema.get(key), (list, dict)) else schema.get(key)
            if info_type is not type(value):
                msg = "Types from information schema and the information retrieved does not match {} {}"
                raise ValueError(msg.format(type(schema.get(key)), type(value)))

            if isinstance(value, (list, dict)):
                result[key] = type(value)()
                self.filter_information(info_retrieved.get(key), schema.get(key), result.get(key))
            else:
                if isinstance(result.get(key, None), list):
                    result[key].append(value)
                else:
                    result[key] = value
        return result

    @auto_tries(RequestException, tries=4, delay=1)
    def http_retrieve(self, url=""):
        r = requests.get(url=url)
        if r.ok:
            return False, r.json()
        else:
            return True, {}

    def get_info(self, url="", information_schema=None):
        error, temperatures_history = self.http_retrieve(url)

        if not temperatures_history or error:
            return True, {}
        else:
            try:
                if information_schema:
                    temperatures_history = self.filter_information(temperatures_history, information_schema)
                return False, temperatures_history
            except (ValueError, KeyError):
                return True, {}

    def store_data(self, data):
        raise NotImplementedError()

    def get_db_connection(self):
        gs = get_global_settings().get("db")
        update = False
        for key in ["password", "username", "host", "db_name"]:
            if gs.get(key) != getattr(self, key, None):
                setattr(self, key, gs.get(key))
                update = True

        if update:
            self.db_url = 'postgresql+pg8000://{username}:{password}@{host}/{db_name}'.format(
                username=self.username,
                password=self.password,
                host=self.host,
                db_name=self.db_name
            )

            self.engine = create_engine(self.db_url)
            self.engine.connect()
            self.base.metadata.bind = self.engine
            self.base.metadata.create_all(self.engine)

    def get_db_session(self):
        self.session = sessionmaker(bind=self.engine)()

    def delete_databases(self):
        table1 = self.base.metadata.tables.get("weatherinfo")
        table2 = self.base.metadata.tables.get("temperature")
        self.engine.execute(table1.delete())
        self.engine.execute(table2.delete())

        # TODO: delete tables with foreign keys later
        # for table in self.base.metadata.sorted_tables:
        #     self.engine.execute(table.delete())