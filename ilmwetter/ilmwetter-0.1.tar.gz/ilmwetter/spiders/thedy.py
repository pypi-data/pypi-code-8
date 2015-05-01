# -*- coding: utf-8 -*-
import scrapy

from ..items import IlmwetterItem


class ThedySpider(scrapy.Spider):
    name = "thedy"
    allowed_domains = [
        "http://www.thedy22.maschinenbau.tu-ilmenau.de/wwwtd/WISI/WISI02.php"]
    start_urls = (
        'http://thedy22.maschinenbau.tu-ilmenau.de/wwwtd/WISI/WISI02.php/',  # noqa
    )

    @staticmethod
    def extract_by_text(response, text):
        return response.xpath("//td[contains(text(), '{text}')]/text()".
                              format(text=text)).\
                              extract()

    @staticmethod
    def extract_by_href(response, text):
        return response.xpath("//a[contains(@href, '{href}')]/text()".
                              format(href=text)).\
                              extract()

    def parse(self, response):
        item = IlmwetterItem()
        item["dew_point"] = self.extract_by_href(response, "taupunkt")
        item["humidity"] = self.extract_by_href(response, "luftfeucht")
        item["precipitation_amount"] = self.extract_by_text(response,
                                                            "Niederschlagsmenge")  # noqa
        item["pressure"] = self.extract_by_text(response, "Luftdruck")
        item["scraping_time"] = self.extract_by_href(response, "GMT")
        item["solar_radiation"] = self.extract_by_text(response,
                                                       "Globalstrahlung")
        item["temperature"] = self.extract_by_text(response, "Lufttemperatur")
        item["wind_direction"] = self.extract_by_text(response, "Windrichtung")
        item["wind_speed"] = self.extract_by_text(response,
                                                  "Windgeschwindigkeit")
        yield item
