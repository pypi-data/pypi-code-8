__author__ = 'kwang'

from abc import ABCMeta, abstractmethod
from pandas import DataFrame
import pandas as pd
from course import *
from catalog import *
from lxml import etree
from crawler import CourseSpider
import os
from datetime import date


class Extractor:
    __metaclass__ = ABCMeta

    name = 'Course Extractor'

    def __init__(self, spider=None, input_directory='raw_output'):
        """

        :param spider: spider
        :type spider: CourseSpider
        :return:
        """
        if spider is None:
            self.input_directory = input_directory
            self.catalog = Catalog()
            self.name = self.input_directory
            self.timestamp = date.today()
        else:
            self.input_directory = spider.get_raw_output()
            self.catalog = Catalog()
            self.name = spider.get_name()
            self.timestamp = spider.get_timestamp()

    def set_input_directory(self, directory):
        # set the directory of raw html files
        self.input_directory = directory

    @abstractmethod
    def extract_each(self, filename):
        """

        :param filename:
        :return: extracted catalog
        :rtype: Catalog
        """
        pass

    def extract_all(self):
        file_list = [self.input_directory+'/' + f for f in os.listdir(self.input_directory)]

        num_files = len(file_list)

        print '[INFO] start extracting from %s' % self.name
        print '[INFO] total files: %d' % num_files

        for each in file_list:
            print '[INFO] processing file: %s, %d remaining' % (each, num_files)
            self.catalog.append_catalog(self.extract_each(each))
            num_files -= 1

        print '[SUMMARY] finished extraction'

    def to_csv(self):
        print '[INFO] saving catalog to file'
        self.catalog.to_csv(self.name+'__'+str(self.timestamp), sep=',')

    def print_result(self):
        print self.catalog


class IllinoisExtractor(Extractor):

    def extract_each(self, filename):
        with open(filename) as f:
            data = f.read()
        try:
            html = etree.HTML(data)
        except:
            return Catalog()
        course_block = html.xpath('//div[@class="courseblock"]')
        course_title = [' '.join(
            etree.HTML(etree.tostring(e)).xpath('//p//strong//text()')
        ).strip() for e in course_block]
        course_desc = [' '.join(
            etree.HTML(etree.tostring(e)).xpath('//p[@class="courseblockdesc"]//text()')
        ) for e in course_block]

        d = DataFrame({'course_title': course_title, 'desc': course_desc})

        d['instructor'] = ''
        d['course_id'] = d['course_title'].apply(
            lambda x: x.encode('utf-8').split('\xe2\x80\x82')[0].replace('\xc2\xa0', ' ')
        )
        d['title'] = d['course_title'].apply(
            lambda x: x.encode('utf-8').split('\xe2\x80\x82')[1].strip()
        )
        d['desc'] = d['desc'].apply(lambda x: x.strip('"').strip())

        d['school'] = 'illinois'

        return Catalog(data=d)


if __name__ == '__main__':
    extractor = IllinoisExtractor(input_directory='raw_output')
    extractor.extract_all()
    extractor.print_result()
    extractor.to_csv()