# -*- coding: utf-8 -*-
from __future__ import absolute_import
import re
import unicodedata
from janome.tokenizer import Tokenizer

from Products.ZCTextIndex.ISplitter import ISplitter
from Products.ZCTextIndex.PipelineFactory import element_factory

ENC = "utf-8"

def process_unicode(s):
    tokenizer = Tokenizer()
    return [t.surface for t in tokenizer.tokenize(s)]

class JanomeSplitter(object):
    """
    Japanese Splitter by janome
    """
    __implements__ = ISplitter

    def process(self, lst):
        """ Will be called when indexing.
        Receive list of str, then return the list of str.
        """
        result = []
        for s in lst:
            if not isinstance(s, unicode):
                s = s.decode(ENC, 'replace')
            # Ignore '*' and '?' globbing
            s.replace(u"?", u"").replace(u"*", u"")
            result += process_unicode(s)
        return result

element_factory.registerFactory('Word Splitter',
                        'JanomeSplitter', JanomeSplitter)
