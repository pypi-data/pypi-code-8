import asyncio
import requests
import sys
import logging
import functools
import time

try:
    import signal
except ImportError:
    signal = None
finally:
    pass

from lxml import etree
from random import randint


class Crawler(object):
    def __init__(self, board):

        self.base_domain = 'https://www.ptt.cc/'
        self.loop = asyncio.SelectorEventLoop()
        asyncio.set_event_loop(self.loop)
        if signal is not None and sys.platform != 'win32':
# yet SIGINT seems some problem, so not to capture it now
            for signame in ['SIGTERM']:
                self.loop.add_signal_handler(getattr(signal, signame), functools.partial(self.signal_captured, signame))

        self.todo = list()
        self.busy = list()
        self.termination = asyncio.locks.Condition()
        self.t0 = time.time()
        self.t1 = None
        self.boardname = board
        # add a initial url to self.todo 
        self.todo.append('/bbs/' + self.boardname + '/index.html')

    def execute_spider(self):
        try:
            self.loop.run_until_complete(self.run_spider(self.boardname))
        except:
            pass
        finally:
            self.close_spider()

    @asyncio.coroutine
    def run_spider(self, board):
        logging.info("spider has started")
        with (yield from self.termination):
            while self.todo or self.busy:
                if self.todo:
                    url = self.todo.pop()
                    yield from Fetcher(self.base_domain + url, self)
                else:
                    logging.info("todo list is empty")
                    yield from self.termination.wait()

    def signal_captured(self, signame):
        logging.info("got singal %s, exit" % signame)
        self.close_spider()

    def stop_spider(self):
        logging.info("spider has stoped")
        self.loop.stop()

    def close_spider(self):
        self.stop_spider()
        logging.info("spider has closed")
        self.t1 = time.time()
        logging.info("used time is %s" % (self.t1 - self.t0))
        self.loop.close()


@asyncio.coroutine
class Fetcher(object):
    cookies = dict(over18="1")
    verify = True

    def __init__(self, url, crawler):
        self.crawler = crawler
        try:
            time.sleep(randint(2,4))
            self.request = requests.get(url, cookies=self.cookies, verify=self.verify)
        except:
            self.request = None
            return None
        finally:
            if self.request.text is not None:
                logging.info("start to parse article list from url %s" % url)
                self.articles = self.parse_article_list(self.request.text)
                logging.debug("fetched article list : %r" % self.articles)
                logging.info('fetched %d articles in %s' % (len(self.articles), url))

    def parse_article_list(self, text):
        logging.info("parsing article info..")
        """return a json with a article list"""
        div_line = None
        html = etree.HTML(text)
        articles = html.xpath('//div[@class="r-list-container bbs-screen"]')[0].getchildren()
        next_node = html.xpath('//div[@class="btn-group pull-right"]')[0].getchildren()[1].attrib['href']
        self.crawler.todo.append(next_node)

        for n in articles:
            if n.attrib['class'] == 'r-list-sep':
                div_line = articles.index(n)
        if div_line is not None:
            articles = articles[:div_line]
        ret = list()
        for article in articles:
            r = dict()
            items = article.getchildren()
            try:
                r['nrec'] = items[0].getchildren()[0].text
            except:
                r['nrec'] = None
            try:
                r['href'] = items[2].getchildren()[0].attrib['href']
            except:
                r['href'] = None
            try:
                r['title'] = items[2].getchildren()[0].text
            except:
                r['title'] = None
            r['date'] = items[3].getchildren()[0].text
            r['author'] = items[3].getchildren()[1].text
            ret.append(r)
        return ret
