from pkg_resources import resource_stream
import unittest

from imsvdex.vdex import VDEXManager
from lxml import etree
from lxml import objectify

class Conversions(unittest.TestCase):
    def testMatrixExport(self):
        manager = VDEXManager(resource_stream(__name__, 'test.xml'))
        data = manager.exportMatrix()
        should_be = [['Level 0', 'Level 1', 'Caption de', 'Description de', 'Caption en', 'Description en', 'Caption fr', 'Description fr', 'Caption it', 'Description it'], ['identical', '', '', '', 'is identical with', '', 'est identique avec', '', u'\xe8 identico con', ''], ['relative', '', 'ist verwandt mit', '', 'is relative of', '', 'est parent avec', '', u'\xe8 parente di', ''], ['', 'child', 'ist Kind von', '', 'is child of', '', 'est enfant de', '', u'\xe8 prole di', '']]
        self.assertEquals(should_be, data)

    def testMatrixImport(self):
        manager = VDEXManager(resource_stream(__name__, 'test.xml'))
        matrix = manager.exportMatrix()
        new_manager = VDEXManager(matrix=matrix)
        self.assertEquals(matrix, new_manager.exportMatrix())

        data = new_manager.serialize()
        should_be_xml = '<?xml version="1.0" encoding="utf-8" ?>\n<vdex xmlns="http://www.imsglobal.org/xsd/imsvdex_v1p0"><term><termIdentifier>identical</termIdentifier><caption><langstring language="en">is identical with</langstring><langstring language="fr">est identique avec</langstring><langstring language="it">\xc3\xa8 identico con</langstring></caption></term><term><termIdentifier>relative</termIdentifier><caption><langstring language="de">ist verwandt mit</langstring><langstring language="en">is relative of</langstring><langstring language="fr">est parent avec</langstring><langstring language="it">\xc3\xa8 parente di</langstring></caption><term><termIdentifier>child</termIdentifier><caption><langstring language="de">ist Kind von</langstring><langstring language="en">is child of</langstring><langstring language="fr">est enfant de</langstring><langstring language="it">\xc3\xa8 prole di</langstring></caption></term></term></vdex>'
        obj = objectify.fromstring(should_be_xml)
        should_be = etree.tostring(obj, encoding='utf-8', standalone=True)
        self.assertEquals(should_be, data)

    def testEmptyMatrix(self):
        manager = VDEXManager()
        matrix = manager.exportMatrix()
        self.assertEquals([], matrix)

    def testOldSyntax(self):
        xml = ''
        lang = 'de'
        self.assertRaises(AttributeError, VDEXManager, xml, lang)

    def testTooMuchInput(self):
        manager = VDEXManager(resource_stream(__name__, 'test.xml'))

        xml = manager.serialize()
        matrix = manager.exportMatrix()
        self.assertRaises(AttributeError, VDEXManager, xml, matrix)
