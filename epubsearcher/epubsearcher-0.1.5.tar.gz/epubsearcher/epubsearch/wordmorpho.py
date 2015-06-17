# -*- coding: utf-8 -*-
import importlib
import logging

class WordMorphoGenerator(object):
    engine = False

    def __init__(self, word, lang='ru'):
        if lang=='ru': engine_name='pymorphy2'
        if engine_name:
            self.word = word

            mod = importlib.import_module("epubsearcher.epubsearch.morpho_engines.%sengine" % engine_name)
            # import whooshengine as engine
            self.engine = getattr(mod,'%sEngine' % engine_name.capitalize())
            logging.info(self.engine)

    def generate(self):
        '''
        run morpho procces for selected engine
        :return: list of words
        '''
        result = self.engine(self.word).process()
        return result