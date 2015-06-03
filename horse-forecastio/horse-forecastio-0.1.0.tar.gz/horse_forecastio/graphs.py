# -*- coding: utf-8 -*-

from datetime import datetime
from cStringIO import StringIO

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

import horse.config
import horse.utils.imgur

from . import ForecastIO


class WeatherGraph(ForecastIO):

    class Meta(ForecastIO.Meta):
        abstract = True

    color = 'b'

    def execute(self, user, channel, operands):
        location = self.geocode(" ".join(operands))
        weather = self.get_current_weather(location)
        data = self.get_data(weather, operands)
        plot = self.draw_plot(data, location)
        url = horse.utils.imgur.post_from_file(plot)
        self.message(channel, url)

    def get_data(self, weather):
        return []

    def get_title(self, location):
        return ""

    def draw_plot(self, data, location):
        output = StringIO()
        with plt.xkcd():
            plt.clf()
            plt.fill_between(data[0], data[1], 0, color=self.color)
            plt.gcf().autofmt_xdate()
            plt.title(self.get_title(location))
            plt.savefig(output, format="png")
        output.seek(0)
        return output


class RainGraph(WeatherGraph):

    class Meta(WeatherGraph.Meta):
        command = 'rain'

    color = 'b'

    def get_title(self, location):
        return "Rain intensity for the next 24 hours in {0}".format(
            location['formatted_address']
        )

    def get_data(self, weather, operands):
        return (
            [
                datetime.fromtimestamp(d['time'])
                for d in weather['hourly']['data'][:24]
            ],
            [
                d['precipIntensity']
                for d in weather['hourly']['data'][:24]
            ]
        )


class TemperatureGraph(WeatherGraph):

    class Meta(WeatherGraph.Meta):
        command = 'temperature'

    color = 'r'

    def get_title(self, location):
        return "Temperature (C) for next 24 hours in {0}".format(
            location['formatted_address']
        )

    def get_data(self, weather, operands):
        return (
            [
                datetime.fromtimestamp(d['time'])
                for d in weather['hourly']['data'][:24]
            ],
            [
                d['temperature']
                for d in weather['hourly']['data'][:24]
            ]
        )
