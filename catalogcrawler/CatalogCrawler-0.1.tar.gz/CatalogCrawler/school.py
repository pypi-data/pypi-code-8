__author__ = 'kwang'

from abc import ABCMeta, abstractmethod
from pandas import DataFrame
from datetime import date
import requests
from lxml import etree
import pred


class School:
    __metaclass__ = ABCMeta

    def __init__(self, info, short_name):
        """
        initialization
        :param info: information needed to gather item urls
        :param short_name: school short name
        :return: None
        :type info: dict
        :type short_name: str
        """
        self.info = info
        self.short_name = short_name
        self.items = self._generate_items()
        self.urls = self.items[['index', 'url']]
        self.timestamp = date.today()

    def to_csv(self, filename, sep='\x1A'):
        output = self.items.copy()
        output["timestamp"] = self.timestamp
        output["shortname"] = self.short_name
        output.to_csv(filename, sep=sep, index=False, encoding="utf-8")

    def print_school_info(self):
        # print out school info
        for key, value in self.info.items():
            print (key, value)

    def print_school_urls(self):
        print self.get_school_urls()

    def print_school_items(self):
        print self.get_school_items()

    def get_school_name(self):
        """
        return the short name of school
        :return: short_name of school
        :rtype: String
        """
        return self.short_name

    def get_school_urls(self):
        """
        return the list of item urls in a DataFrame
        :return: list of item urls
        :rtype: DataFrame (columns = ['index', 'url']
        """
        return self.urls

    def get_school_items(self):
        """

        :return: Items as a DataFrame
        :rtype: DataFrame
        """
        return self.items

    def get_timestamp(self):
        """

        :return: timestamp
        :rtype: date
        """

    @abstractmethod
    def _generate_items(self):
        """
        Generate the list of items info as a DataFrame with one column named url
        to be implemented for each different subclasses
        :rtype : DataFrame
        """
        pass


class HTMLSchool(School):
    """
    required in 'info' at initialization:
     parent_url
     base_url
     item_xpath - xpath to extract url items
     category_xpath - xpath to extract item category
     url_xpath - xpath to extract urls
    """
    required_fields = [
        'parent_url',
        'base_url',
        'item_xpath',
        'category_xpath',
        'url_xpath'
    ]

    def _generate_items(self):
        """
        implementation of generating school items
        :return: list of items in DataFrame with one column for url named 'url'
        :rtype: DataFrame
        """
        for each in HTMLSchool.required_fields:
            if each not in self.info.keys():
                raise Exception("HTMLSchool requires field %s in info" % each)

        parent_url = self.info['parent_url']
        base_url = self.info['base_url']
        item_xpath = self.info['item_xpath']
        category_xpath = self.info['category_xpath']
        url_xpath = self.info['url_xpath']

        r = requests.get(url=parent_url, headers=pred.HEADERS)
        if r.status_code != 200:
            raise Exception("Cannot connect to parent_url %s" % parent_url)

        res = r.text
        html = etree.HTML(res)

        items = html.xpath(item_xpath)

        category = [' '.join(e.xpath(category_xpath)) for e in items]
        pid = [' '.join(e.xpath(url_xpath)) for e in items]
        url = [base_url + e for e in pid]

        url_list = DataFrame(
            {'category': category, 'url': url, 'pid': pid}, columns=['pid', 'category', 'url']
        ).reset_index()
        return url_list


class SitemapSchool(School):
    required_fields = [
        'sitemap',
        'base_url',
        'multi_page'
    ]

    def _generate_items(self):
        for each in SitemapSchool.required_fields:
            if each not in self.info.keys():
                raise Exception("SitemapSchool requires the field %s" % each)

        sitemap = self.info['sitemap']
        base_url = self.info['base_url']
        multi_page = self.info['multi_page']

        r = requests.get(sitemap, headers=pred.HEADERS)

        if r.status_code != 200:
            raise Exception("Cannot connect to %s" % r.url)

        sitemap_list = etree.XML(r.text.encode('utf-8')).xpath('//*/text()')
        url = [s for s in sitemap_list if base_url in s]

        if multi_page == 0:
            return DataFrame({'url': url})

        urls = []
        for each in url:
            try:
                r = requests.get(each, headers=headers)
                links = etree.XML(r.text.encode('utf-8')).xpath('//*/text()')
                urls = urls + [u for u in links if u.startswith('http')]
            except:
                continue

        return DataFrame({'url': urls}).reset_index()


if __name__ == '__main__':
    info = {
        'parent_url': 'http://catalog.illinois.edu/courses-of-instruction/',
        'base_url': 'http://catalog.illinois.edu',
        'item_xpath': '//li//a',
        'category_xpath': 'text()',
        'url_xpath': '@href'
    }
    p = HTMLSchool(info=info, short_name='illinois')
    print p.get_school_items()
    print p.get_school_urls()
    print p.get_school_name()

    info = {
        'sitemap': 'https://www.udemy.com/sitemap.xml',
        'base_url': 'https://www.udemy.com/sitemap/courses.xml?p=',
        'multi_page': 1
    }
    p = SitemapSchool(info=info, short_name='udemy')
    print p.get_school_items()
    print p.get_school_urls()
    print p.get_school_name()