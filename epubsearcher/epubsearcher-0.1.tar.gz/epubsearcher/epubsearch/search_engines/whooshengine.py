from whoosh.index import create_in
import whoosh.index as index
from whoosh.fields import Schema, TEXT, ID
from bs4 import BeautifulSoup
from whoosh.qparser import QueryParser
from .baseengine import BaseEngine
import os
import re
import logging


class WhooshEngine(BaseEngine):
    # whoosh
    schema = Schema(title=TEXT(stored=True), path=TEXT(stored=True), href=ID(stored=True), cfiBase=TEXT(stored=True), spinePos=TEXT(stored=True), content=TEXT)

    def open(self):
        try:
            self.ix = index.open_dir(self.database_path)
        except Exception as e:
            logging.error("openning database {} failed".format(self.database_name))

    def create(self):

        if not os.path.exists(self.database_path):
            os.mkdir(self.database_path)

        try:
            logging.debug("openning database {} to create".format(self.database_name))
            self.ix = index.create_in(self.database_path, self.schema)
        except Exception as e:
            logging.error(e)

        self.writer = self.ix.writer()

    def add(self, path='', href='', title='', cfiBase='', spinePos=''):
        text = self.__get_text(path)
        self.writer.add_document(title=str(title), path=str(path), href=str(href), cfiBase=str(cfiBase), spinePos=str(spinePos), content=str(text))
        logging.debug("Indexed: " + title + ' | ' + path + ' | ' + href + ' | ' + str(spinePos))

    def finished(self):
        self.writer.commit()

    def query(self, q, limit=None):
        logging.debug('Q {}'.format(q))
        with self.ix.searcher() as searcher:
            results = []
            parsed_query = QueryParser("content", schema=self.ix.schema).parse(q)
            hits = searcher.search(parsed_query, limit=limit)
            logging.debug("Hits {}".format(hits))
            for hit in hits:
                item = {}
                item['title'] = hit["title"].encode("utf-8")
                item['href'] = hit["href"].encode("utf-8")
                item['path'] = hit["path"].encode("utf-8")
                item['cfiBase'] = hit["cfiBase"].encode("utf-8")
                item['spinePos'] = hit["spinePos"].encode("utf-8")
                results.append(item)

            return results

    def __get_text(self, filename):
        # html = urllib.urlopen('http://www.nytimes.com/2009/12/21/us/21storm.html').read()
        html = open(filename, "r")
        soup = BeautifulSoup(html)
        texts = soup.findAll(text=True)

        def visible(element):
                if element.parent.name in ['style', 'script', '[document]', 'head', 'title']:
                        return False
                elif re.match('<!--.*-->', str(element.encode('utf-8'))):
                        return False
                return True

        visible_texts = filter(visible, texts)

        contents = ' '.join([s for s in visible_texts])

        return contents.strip() #.encode('utf-8')
