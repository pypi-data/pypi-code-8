# -*- coding: utf-8 -*-
#/usr/bin/python

'''
Created on 23/06/2015

.. moduleauthor:: licface <licface@yahoo.com>

:synopsis:
    Get return your pub key from keyserver.ubuntu.com
    and add it to apt-key add [pub key]
    moreover you can save on file or copy it to the clipboard
    optional use can install 'requests' module
    default use urllib2 module
'''
import sys
try:
    import requests
except:
    import urllib2
from bs4 import BeautifulSoup as bs
import argparse
import clipboard


class handle:
    '''
        .. codeauthor:: licface <licface@yahoo.com>

        :returns: None

        :raise: None
    '''
    def __init__(self, handle=None):
        '''

        :param handle: handle = None
        :type handle: None

        :returns: None

        :raise: None
        '''

        self.handle = handle
        if handle is None:
            self.handle = 'urllib2'

        self.module = __import__(self.handle)

    def checkSite(self, url):
        '''

        :param url: http://www.example.com
        :type url: str

        :returns: Bool

        :raise: Traceback
        '''
        if self.handle == 'requests':
            try:
                self.module.get(url)
                return self.module.get(url).ok
            except:
                return False
        else:
            try:
                self.module.urlopen(url)
                return True
            except:
                return False

    def getSite(self, url):
        '''

        :param url: http://www.example.com
        :type url: str

        :returns: bool or str (content)

        :raise: Traceback
        '''
        if self.handle == 'requests':
            try:
                self.module.get(url)
                return self.module.get(url).text
            except:
                try:
                    return urllib2.urlopen(url).read()
                except:
                    return False
        else:
            try:
                self.module.urlopen(url)
                return self.module.urlopen(url).read()
            except:
                return False


class generator(object):
    '''
    .. codeauthor:: licface <licface@yahoo.com>
    '''

    def __init__(self):
        '''
        __init__
        :returns: None

        :raise: Traceback
        '''
        super(generator, self)
        self.handle = handle('requests')

    def getSite(self, key, copytoclipboard=None):
        '''
        .. codeauthor:: Firstname Lastname <firstname@example.com>

        :param key: string number
        :type key: string

        :returns: str

        :raise: Traceback
        '''
        url = 'http://keyserver.ubuntu.com/pks/lookup?op=get&search=0x{0}'.format(key)
        site = self.handle.getSite(url)
        if site is not False:
            soup = bs(site)
            data1 = soup.find("pre")
            if copytoclipboard:
                clipboard.copy(unicode(data1.contents[0]).encode('UTF-8'))
            return unicode(data1.contents[0]).encode('UTF-8')
        else:
            return ''

    def usage(self):
        '''
        usage: generator.py [-h] [-k KEY] [-c] [-f FILENAME]

        optional arguments:
          -h, --help            show this help message and exit
          -k KEY, --key KEY     Key number for search pub key
          -c, --copy            Copy pub key result to clipboard
          -f FILENAME, --file FILENAME
                                Store pub key result to file


        :returns: str (Usage help)

        :raise: Traceback
        '''
        parser = argparse.ArgumentParser()
        parser.add_argument('-k', '--key', help='Key number for search pub key', action='store')
        parser.add_argument('-c', '--copy', help='Copy pub key result to clipboard', action='store_true')
        parser.add_argument('-f', '--file', help='Store pub key result to file', action='store', dest='filename', type=argparse.FileType('w'))
        if len(sys.argv) == 1:
            parser.print_help()
        else:
            args = parser.parse_args()
            if args.key:
                if args.filename:
                    data = self.getSite(args.key, args.copy)
                    args.filename.write(data)
                else:
                    self.getSite(args.key, args.copy)
            else:
                parser.print_help()

def main():
    c = generator()
    c.usage()

if __name__ == '__main__':
    main()


