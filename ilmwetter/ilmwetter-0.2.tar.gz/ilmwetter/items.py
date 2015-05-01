# -*- coding: utf-8 -*-
import scrapy


class IlmwetterItem(scrapy.Item):
    dew_point = scrapy.Field()
    humidity = scrapy.Field()
    precipitation_amount = scrapy.Field()
    pressure = scrapy.Field()
    scraping_time = scrapy.Field()
    solar_radiation = scrapy.Field()
    temperature = scrapy.Field()
    wind_direction = scrapy.Field()
    wind_speed = scrapy.Field()
