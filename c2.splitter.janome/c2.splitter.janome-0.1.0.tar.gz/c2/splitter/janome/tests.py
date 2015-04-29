import unittest

from zope.testing import doctestunit
from zope.component import testing
from Testing import ZopeTestCase as ztc

from Products.Five import zcml
from Products.Five import fiveconfigure
from Products.PloneTestCase import PloneTestCase as ptc
from Products.PloneTestCase.layer import PloneSite
from Products.CMFCore.utils import getToolByName

ptc.setupPloneSite()

import c2.splitter.janome

class TestCase(ptc.PloneTestCase):
    class layer(PloneSite):
        @classmethod
        def setUp(cls):
            fiveconfigure.debug_mode = True
            zcml.load_config('configure.zcml',
                             c2.splitter.janome)
            fiveconfigure.debug_mode = False

        @classmethod
        def tearDown(cls):
            pass


class TestCanUseSpritter(TestCase):
    """Can Replace the catalog """
    def afterSetUp(self):
        pass

    def testWordSplitter(self):
        from Products.ZCTextIndex.PipelineFactory import element_factory
        group = 'Word Splitter'
        names = element_factory.getFactoryNames(group)
        self.failUnless('JanomeSplitter' in names)

    def testNounSearchableText(self):
        cat = getToolByName(self.portal, 'portal_catalog')
        # Create index
        from Products.ZCTextIndex.OkapiIndex import OkapiIndex
        from Products.ZCTextIndex.ZCTextIndex import PLexicon
        from Products.ZCTextIndex.ZCTextIndex import ZCTextIndex
        lexicon = PLexicon('janome_lexicon', '', c2.splitter.janome.janome.Normalizer())
        cat._setObject('janome_lexicon', lexicon)
        i = ZCTextIndex('NounSearchableText', caller=cat,
                index_factory=OkapiIndex,
                lexicon_id=lexicon.id)
        cat.addIndex('NounSearchableText', i)

        self.failUnless('NounSearchableText' in cat.indexes())
        self.failUnless('janome_lexicon' in
                        [ix.getLexicon().id for ix in cat.index_objects()
                         if ix.id == 'NounSearchableText'])

class TestJanomeFunctions(unittest.TestCase):
    """Test for Functions"""
    def afterSetUp(self):
        pass

    def test_process_unicode(self):
        process_unicode = c2.splitter.janome.janome.process_unicode
        self.assertEqual(process_unicode(
            u"ここはPloneシンポジウムのサイトです",
            ['ここ', 'は', 'Plone', 'シンポジウム', 'の', 'サイト', 'です'])
        )

def test_suite():
    return unittest.TestSuite([

        unittest.makeSuite(TestCanUseSpritter),
        unittest.makeSuite(TestJanomeFunctions),

        ])

if __name__ == '__main__':
    unittest.main(defaultTest='test_suite')
