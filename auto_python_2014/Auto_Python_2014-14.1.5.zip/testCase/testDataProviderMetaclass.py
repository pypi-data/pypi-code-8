'''
Created on 2014-12-17

@author: zhangziteng
'''
import unittest
from component.CPT_api_request import APIrequest 


class DataProviderSupport(type):
    def __new__(meta, classname, bases, classDict):
        # method for creating our test methods
        def create_test_method(testFunc, args):
            return lambda self: testFunc(self, *args)

        # look for data provider functions
        for attrName, attr in classDict.items():
            print type(meta)
            print type(classname)
            print type(bases)
            print type(classDict)
            print "attrName "+str(attrName)
            print "attr "+str(attr)
            if attrName.startswith("dataprovider_"):
                # find out the corresponding test method
                testName = attrName[13:]
                testFunc = classDict[testName]
                print "   testName "+testName
                print "   testFunc "+str(testFunc)
                # the test method is no longer needed
                del classDict[testName]

                # generate test method variants based on
                # data from the data porovider function
                i = 1
                for args in attr():
                    print args
                    print attr()
                    print testName
                    classDict[testName + str(i)] = create_test_method(testFunc, args)
                    i += 1
                
        # create the type
        return type.__new__(meta, classname, bases, classDict)


class TestStringLength(unittest.TestCase):
    __metaclass__ = DataProviderSupport

    def dataprovider_test_len_function(): # no self!
        yield ("abc", 3)
        yield ("", 0)
        yield ("a", 1)

    def test_len_function(self, astring, expectedLength):
        #print __metaclass__.__name__
        print "astring "+astring+":"+"expectedLength "+str(expectedLength)
        self.assertEqual(expectedLength, len(astring))
        
    def dataprovider_test_len_functionnnnn(): # no self!
        yield ("abc", 3)
        yield ("", 0)

    def test_len_functionnnnn(self, astring, expectedLength):
        #print __metaclass__.__name__
        print "astring "+astring+":"+"expectedLength "+str(expectedLength)
        self.assertEqual(expectedLength, len(astring))

    def setUp(self):
        #tapirequest = APIrequest()
        #tapirequest.cpt_createdbconnection()
        #tapirequest.cpt_getall(sql)
        pass


    def tearDown(self):
        pass


    def testName(self):
        pass


if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()