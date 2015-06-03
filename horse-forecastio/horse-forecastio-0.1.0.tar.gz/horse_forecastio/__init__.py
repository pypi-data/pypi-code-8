# -*- coding: utf-8 -*-

import logging
import requests

import horse.config
import horse.utils.imgur
from horse.bridles.base import CommandBridle


class ForecastIO(CommandBridle):

    class Meta(CommandBridle.Meta):
        command = 'weather'
        description = "Pulls and represents weather info from forecast.io"
        help_text = ["Usage: `/horse weather [address]`"]

        display_name = "Weather Forecast"
        display_icon = "http://ryangrieve.com/labs/slack_icons/weather.png"

    def __init__(self, jockey):
        super(ForecastIO, self).__init__(jockey)

    def geocode(self, address):
        details = requests.get(
            'https://maps.googleapis.com/maps/api/geocode/json',
            params={
                'address': address,
                'key': horse.config.GAPI_API_TOKEN
            }
        )
        if details.status_code != 200:
            logging.error(details.content)
            return None
        else:
            results = details.json()['results']

        if len(results) == 0:
            return None
        else:
            return results[0]

    def get_current_weather(self, location):
        url = "https://api.forecast.io/forecast/{0}/{1}?units=si".format(
            horse.config.FORECASTIO_API_TOKEN,
            '{lat},{lng}'.format(**location['geometry']['location'])
        )
        response = requests.get(url)
        if response.status_code == 200:
            forecast = response.json()
            return forecast
        else:
            return None

    def execute(self, user, channel, operands):
        location = self.geocode(" ".join(operands))
        if location is None:
            return "Could not find that location"
        weather = self.get_current_weather(location)
        header = u"*{0}*: _{1}_, {2}°C".format(
            location['formatted_address'],
            weather['currently']['summary'],
            weather['currently']['temperature'],
        )
        body = ""
        for period in ['minutely', 'hourly', 'daily']:
            if period in weather:
                body += weather[period]['summary'] + " "

        msg = header + '\n' + body
        self.message(channel, msg)
