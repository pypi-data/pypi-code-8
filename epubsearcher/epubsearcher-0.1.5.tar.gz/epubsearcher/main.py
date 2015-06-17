import zipfile
import shutil
import os

import logging
import logging.handlers

from optparse import OptionParser

try:
    from .epubsearch import EpubParser
    from .epubsearch import EpubIndexer
    from .epubsearch import WordMorphoGenerator
except:
    from epubsearch import EpubParser
    from epubsearch import EpubIndexer
    from epubsearch import WordMorphoGenerator

syslog = logging.handlers.SysLogHandler(address = '/dev/log')
logging.basicConfig(format="%(levelname)s:%(asctime)s %(message)s datefmt='%Y-%m-%dT%H:%M:%S'",  level=logging.DEBUG,
                    handlers=[syslog])


def unzip(source_filename, dest_dir):
    with zipfile.ZipFile(source_filename) as zf:
        path = dest_dir
        zf.extractall(path)


class EpubWorker(object):
    """
    This module is main class. For using as library needed import this class.
    @:book_address - address for dir or compressed epub publication
        :parameter "./test_data/Sensei4.epub"
    @:lang - need for generating lexemes
        :parameter "ru" or "en"
    @:force_index - if you need force reindex book
        :parameter True/False
    """
    def __init__(self, book_address, lang='ru', force_index=False):
        force_index=force_index
        self.is_epub = False
        epub_worker_folder = "/tmp/epub_worker"
        if not os.path.exists(epub_worker_folder):
            os.mkdir(epub_worker_folder)

        if book_address[-4:] == 'epub':
            self.is_epub = True
            logging.info('Uncompress {}'.format(book_address))
            book_name = book_address[book_address.rfind('/')+1:-5]
            self.dest_dir = '/tmp/epub_worker/temp/'+book_name
            unzip(book_address, self.dest_dir)
            book_address = self.dest_dir
        else:
            book_name = book_address[book_address.rfind('/')+1:]

        self.epub = EpubParser(book_address)
        self.index = EpubIndexer(engine_name='whoosh', database_name=book_name, force_index=force_index)
        logging.info('Indexing')
        self.index.load(self.epub)

    def search_word(self, search_word):
        logging.info('Search word {}'.format(search_word))
        return self.index.search(search_word)

    def search_lexemes(self, search_word):
        logging.info('Generate words for search')
        search_words = WordMorphoGenerator(search_word).generate()
        logging.info('Search word {} and lexemes'.format(search_word, search_words))
        results_dirty = []
        results_formatted = []
        for word in search_words:
            results_dirty.append(self.index.search(word))
        for result in results_dirty:
            result = result.get('results')
            if result:
                for item in result:
                    results_formatted.append({'baseCfi': item['baseCfi'],
                                              'cfi': item['cfi'],
                                              'href': item['href'],
                                              'path': item['path']})

        return {'word': search_word,
                'lexemes': search_words,
                'results': results_formatted}

    def get_chapters_cfi(self):
        spine = self.epub.spine
        characters_cfi = [row['cfiBase'] for row in spine]
        return characters_cfi

    def close(self):
        shutil.rmtree(self.dest_dir)

    def __enter__(self):
        return self

    def __exit__(self, type, value, traceback):
        if self.is_epub:
            shutil.rmtree(self.dest_dir)



def get_parameters():
    """
        Parse the user input
    """
    parser = OptionParser()
    parser.add_option('-b', '--book-address', dest='book_address')
    parser.add_option('-s', '--search', dest='search')
    parser.add_option('-f', '--force-index', dest='force_index')
    parser.add_option('--lang', dest='language')
    parser.add_option('--lexemes', dest='lexemes')
    (options, args) = parser.parse_args()

    if not options.book_address:
        options.book_address = "Sensei4/"
    else:
        return {'book_address': options.book_address,
                'search': options.search, 'language': options.language,
                'lexemes': options.lexemes, 'force_index': options.force_index}


def main():
    logging.info('*'*20)
    # get user defined parameters
    userParams = get_parameters()

    search = userParams['search']
    book_address = userParams['book_address']
    language = userParams['language']
    lexemes = userParams['lexemes']
    force_index = userParams['force_index']

    with EpubWorker(book_address, language, force_index) as worker:
        if lexemes:
            return worker.search_lexemes(search)
        return worker.search_word(search)

if __name__ == '__main__':
    # logging.basicConfig(format='%(levelname)s:%(asctime)s %(message)s', level=logging.DEBUG)
    print(main())

