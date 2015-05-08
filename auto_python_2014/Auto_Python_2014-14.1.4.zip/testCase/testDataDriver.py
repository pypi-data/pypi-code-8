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
                testtbName = testName[4:]
                # the test method is no longer needed
                del classDict[testName]
                #apidata.cpt_getcounts(testtbName)
                #apidata.cpt_getsn(testtbName)
                apidata.cpt_getusers()
                for user in apidata.users:
                    #print "00000000000000000000000000000000",user
                    apidata.cpt_getsn(testtbName,user)
                    #print testtbName,user,apidata.sn
                    #print apidata.sn
                    # generate test method variants based on
                    # data from the data porovider function
                    i = 1
                    #for args in tuple(apidata.sn):
                        #print args
                    #print apidata.sn
                    for args in tuple(apidata.sn):
                        #print "8888888888",args
                        #print args[1]
                        #print testName + "__"+str(i)+"__"+user+"_"+str(args[1])
                        #print "***********************"
                        classDict[testName + "__"+str(i)+"__"+user+"_"+str(args[1])] = create_test_method(testFunc, args)
                        i += 1
                    i = 1

        # create the type
        return type.__new__(meta, classname, bases, classDict)

class Testdriver(unittest.TestCase):
    __metaclass__ = DataProviderSupport
        
    def setUp(self):
        global _apitest
        _apitest = APIrequest()

    def dataprovider_testdh_item_get_20():
        pass
    def testdh_item_get_20(self,tbname,rowindex):
        #global_apitest = APIrequest()
        #print _apitest.username
        _apitest.cpt_api_getresponse(tbname,rowindex)
        self.assertEqual(_apitest.chck, _apitest.dictdecoderesponsestr, "expect is :\n"+_apitest.chck+ "\n but actual :\n"+_apitest.dictdecoderesponsestr)
    
    def dataprovider_testdh_item_get_00():
        pass
    def testdh_item_get_00(self,tbname,rowindex):
        _apitest.cpt_api_getresponse(tbname,rowindex)
        self.assertEqual(_apitest.chck, _apitest.dictdecoderesponsestr, "expect is :\n"+_apitest.chck+ "\n but actual :\n"+_apitest.dictdecoderesponsestr)
    
    def testName(self):
        pass
    
    def dataprovider_testdh_item_html_get_20():
        pass
    def testdh_item_html_get_20(self,tbname,rowindex):
        pass

    def dataprovider_testdh_message_status_update_20():
        pass
    def testdh_message_status_update_20(self,tbname,rowindex):
        _apitest.cpt_api_getresponse(tbname,rowindex)
        self.assertEqual(_apitest.chck, _apitest.dictdecoderesponsestr, "expect is :\n"+_apitest.chck+ "\n but actual :\n"+_apitest.dictdecoderesponsestr)

    def dataprovider_testdh_message_count_list_20():
        pass
    def testdh_message_count_list_20(self,tbname,rowindex):
        _apitest.cpt_api_getresponse(tbname,rowindex)
        self.assertEqual(_apitest.chck, _apitest.dictdecoderesponsestr, "expect is :\n"+_apitest.chck+ "\n but actual :\n"+_apitest.dictdecoderesponsestr)

if __name__ == '__main__':
    
    suite=unittest.TestSuite()   #定义一个单元测试容器
    #print suite
    #suite.addTest(Testdriver("testName"))
    #suite.addTest(ParametrizedTestCase.parametrize(Testdriver,param="tablename"))
    #suite.addTest(Testdriver("test_dh_item_get_20_1"))
    suite.addTest(Testdriver("testdh_item_get_20"))
    #suite.addTest(Testdriver("testdh_item_get_00"))
    unittest.TextTestRunner(verbosity=2).run(suite)
    #unittest.main()
    