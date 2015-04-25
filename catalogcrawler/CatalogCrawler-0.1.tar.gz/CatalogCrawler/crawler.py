__author__ = 'kwang'

from school import *
import requests
import pandas as pd
from pandas import DataFrame
import os
import pred
import time
from datetime import date


class CourseSpider():

    name = 'Course Spider'

    def __init__(self, school, raw_output, log):
        """

        :param school: school to crawl
        :type school: School
        :param raw_output: directory for raw html crawled
        :type raw_output: str
        :param log: file to log failed cases
        :type log: str
        :return: None
        """

        self.name = school.get_school_name()
        self.urls = school.get_school_urls()
        self.raw_output = raw_output
        self.log = log
        self.timestamp = school.get_timestamp()

    def __init__(self, filename, raw_output, log, sep='\x1A'):
        self.name = filename
        self.raw_output = raw_output
        self.log = log
        urls = pd.read_csv(self.name, sep=sep, encoding='utf-8')[['index', 'url']]
        self.urls = urls
        self.timestamp = date.today()

    def get_raw_output(self):
        return self.raw_output

    def get_name(self):
        return self.name

    def get_timestamp(self):
        return self.timestamp

    def crawl_url(self, url, fname):
        """

        :param url:
        :param fname:
        :return: status code
            0 - success
            1 - non-200 status code
            2 - error in requests get
        """
        if not os.path.isdir(self.raw_output):
            os.makedirs(self.raw_output)

        print '[INFO] crawling: %s' % url
        try:
            r = requests.get(url, headers=pred.HEADERS)
        except:
            return 2
        if r.status_code != 200:
            with open(self.log, 'a') as f:
                f.write(url)
                f.write('\n')
            return 1
        with open(self.raw_output+'/'+fname, 'w') as f:
            f.write(r.text.encode('utf-8'))
        return 0

    def crawl_all(self):
        if not os.path.isdir(self.raw_output):
            os.makedirs(self.raw_output)

        file_list = os.listdir(self.raw_output)

        i = 0
        for each in self.urls.itertuples():
            file_name = str(each[1])
            url = each[2]

            if file_name in file_list:
                print '[INFO] file already exists, skip'
                continue

            crawl_status = self.crawl_url(url=url, fname=file_name)
            if crawl_status == 2:
                time.sleep(10)
                self.crawl_url(url=url, fname=file_name)
            i += 1

        print '[SUMMARY] crawl %s complete' % self.name
        print '[SUMMARY] crawled %d pages' % i
        print '[SUMMARY] result generated at %s' % self.raw_output


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

    p.to_csv(filename='illinois')

    crawl = CourseSpider(filename='illinois', sep='\x1A', raw_output='raw_output', log='log.txt')
    crawl.crawl_all()