# -*- coding: utf-8 -*-
from datetime import datetime


class IlmwetterPipeline(object):
    @staticmethod
    def process_float(item, attr):
        item[attr] = float(item[attr][1].split()[0])

    def process_item(self, item, spider):
        timetext = item["scraping_time"][0]
        raw_date, raw_time = timetext.split("am")[1].split("um")
        int_dates = map(int, raw_date.split("."))
        int_dates.reverse()
        int_times = map(int, raw_time.split(":")[:2])
        item["scraping_time"] = datetime(*(int_dates + int_times))

        for attr in ("temperature", "humidity", "dew_point", "pressure",
                     "wind_direction", "wind_speed", "solar_radiation",
                     "precipitation_amount"):
            self.process_float(item, attr)

        return item
