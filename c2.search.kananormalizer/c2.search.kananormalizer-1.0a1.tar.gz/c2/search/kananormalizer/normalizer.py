# -*- coding: utf-8 -*-
from Products.ZCTextIndex.PipelineFactory import element_factory
from plone.i18n.normalizer.base import baseNormalize

KANA_MIN = ord(u"ア")
KANA_MAX = ord(u"ア") + 85
KANA_DIF = ord(u"あ") - ord(u"ア")

class KanaNormalizer(object):

    def process(self, lst):
        enc = 'utf-8'
        result = []
        for s in lst:
            try:
                if not isinstance(s, unicode):
                    s = unicode(s, enc)
            except (UnicodeDecodeError, TypeError):
                pass

            if 0x41 <= ord(s[0]) <= 0x24F:
                # normalize latin words
                # words beginning with a latin character
                # are commonly latin words
                s = baseNormalize(s).lower()
            s = ''.join(unichr(ord(x) + KANA_DIF)
                            if KANA_MIN <= ord(x) <= KANA_MAX
                                else x for x in s)

            result.append(s.lower())

        return result

try:
    element_factory.registerFactory('Case Normalizer',
        'Unicode Ignoring Accents Case Normalizer with Japanese Kana Normalizer', KanaNormalizer)
except ValueError:
    # In case the normalizer is already registered, ValueError is raised
    pass
