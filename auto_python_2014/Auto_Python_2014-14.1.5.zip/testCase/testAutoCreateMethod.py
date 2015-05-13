#coding=utf-8
import unittest
from component.CPT_api_request import APIrequest



class DataProviderSupport(type):
    def __new__(meta, classname, bases, classDict):
        # create testdata
        apidata = APIrequest()
        apidata.cpt_createdbconnection()
        # method for creating our test methods
        def create_test_method(testFunc, args):
            return lambda self: testFunc(self, *args)
        # look for data provider functions
        for attrName, attr in classDict.items():
            if attrName.startswith("dataprovider_"):
                # find out the corresponding test method
                testName = attrName[13:]
                print testName
                testFunc = classDict[testName]
                print testFunc
                # the test method is no longer needed
                del classDict[testName]
                apidata.cpt_getapinames()
                #print apidata.users
                for apiname in apidata.apinames:
                    apidata.cpt_getmobilesn(apiname)
                    #print user
                    print "***********"
                    print apidata.sn
                    print "***********"
                    # generate test method variants based on
                    # data from the data porovider function
                    i = 1
                    for args in tuple(apidata.sn):
                        #create an testfunction and the args
                        #in args include tuple like [(tbname,1),(tbname,2)]
                        print args
                        print tuple(apidata.sn)
                        print "============"
                        print apidata.sn
                        print "============"
                        testName = "test"+str(args[0]) + "__"+str(args[1])
                        classDict[testName] = create_test_method(testFunc, args)
                        i += 1
                        print classDict
                    i = 1

                #print "=================="
                print classDict
        # create the type
        return type.__new__(meta, classname, bases, classDict)

class Testdriver(unittest.TestCase):
    __metaclass__ = DataProviderSupport

    def setUp(self):
        global _apitest
        _apitest = APIrequest()

    def dataprovider_testMethod():
        pass
    def testMethod(self,tbname,rowindex):
        _apitest.cpt_mobileapi_getresponse(tbname,rowindex)
        self.assertEqual(_apitest.chck, _apitest.dictdecoderesponsestr, "expect is :\n"+_apitest.chck+ "\n but actual :\n"+_apitest.dictdecoderesponsestr)

'''
if __name__ == '__main__':
    #suite=unittest.TestSuite()
    #suite.addTest(Testdriver("testdhnew_items_get"))
    #print "********************"
    suite=unittest.TestSuite()   #定义一个单元测试容器
    suite.addTest(Testdriver("dhnew_items_get__3"))
    unittest.TextTestRunner(verbosity=2).run(suite)
'''

'''
    #suite=unittest.TestSuite()
    #suite.addTest(Testdriver("testdhnew_items_get"))
    #unittest.TextTestRunner(verbosity=2).run(suite)
    tTest = Testdriver()
    suite=unittest.TestSuite()
    suite.addTest(tTest("testdhnew_items_get"))
    runner = unittest.TextTestRunner(verbosity=2)
    runner.run(suite)
'''