from open_weather_forecast.info_extractor.get_info import GetInfo


class GetTemperature(GetInfo):

    def __init__(self):
        super(GetTemperature).__init__()
        self.db = None

    def store_data(self, data):
        self.get_db_connection()
        import ipdb
        ipdb.set_trace()

