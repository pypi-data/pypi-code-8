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
                testFunc = classDict[testName]
                testtbName = testName[4:]
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
                        classDict[testName + "__"+str(args[1])] = create_test_method(testFunc, args)
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

    def dataprovider_testdhnew_items_get():
        pass
    def testdhnew_items_get(self,tbname,rowindex):
        #global_apitest = APIrequest()
        #print _apitest.username
        _apitest.cpt_mobileapi_getresponse(tbname,rowindex)
        self.assertEqual(_apitest.chck, _apitest.dictdecoderesponsestr, "expect is :\n"+_apitest.chck+ "\n but actual :\n"+_apitest.dictdecoderesponsestr)


'''
if __name__ == '__main__':
    suite=unittest.TestSuite()   #定义一个单元测试容器
    #suite.addTest(Testdriver("testdh_buyer_search_product_10"))
    unittest.TextTestRunner(verbosity=2).run(suite)
'''
    