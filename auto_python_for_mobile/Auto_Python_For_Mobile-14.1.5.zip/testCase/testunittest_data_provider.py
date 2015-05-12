'''
Created on 2014-12-18

@author: zhangziteng
'''
import unittest
from unittest_data_provider import data_provider

class CssParserTest(unittest.TestCase):
    itemIds = lambda: (('q42',), ('Q42',), ('Q1', ), ('Q1000',), ('Q31337',),)
        
    colors = lambda: (
        ( (0, 0, 0), '#000' ),
        ( (0, 0, 0), '#000000' ),
        ( (0, 0, 0), 'rgb(0, 0, 0)' ),
        ( (0, 0, 0), 'black' )
    )

    @data_provider(itemIds)
    def test_parse_color(self, itemstring):
        print itemstring
        #self.assertEquals(it.getSerialization, itemstring)


if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()