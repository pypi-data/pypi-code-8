#coding=utf-8
import unittest
import lib.HTMLTestRunner
from testDataDriver import Testdriver
import time
import sys,os
from component.CPT_driver_cases import Drivergetcase

reload(sys)
sys.setdefaultencoding('utf-8')

def htr(username):
    tdrivergetcase=Drivergetcase()
    tdrivergetcase.cpt_setUsername(username)
    tdrivergetcase.cpt_createdbconnection()
    tdrivergetcase.cpt_getcases()
    #for dicts in tdrivergetcase.results:
    #    print dicts
    #    print dicts["casename"]
    tdrivergetcase.cpt_getcases_data()
    #print tdrivergetcase.resultsdata
    #Testdriver('test_dh_item_get_00__1')
    #print sys.path[0]
    localtimes = time.strftime('%Y-%m-%d_%H-%M-%S',time.localtime(time.time()))
    suite=unittest.TestSuite()   #定义一个单元测试容器
    #testunit.addTest(testDataDriver('test_dh_item_get_20'))  #将测试用例加入到测试容器中
    #i=1
    #while i<9:
    #    suite.addTest(Testdriver('test_dh_item_get_20'+'__'+str(i)))
    #    i+=1
        #suite.addTest(Testdriver('test_dh_item_get_20_2'))
    #suite.addTest(Testdriver('test_dh_item_get_00__1'))
    #suite.addTest(Testdriver('test_dh_item_get_00__2'))
    for case in tdrivergetcase.results:
        #print case["casename"]
        i=1
        for item in tdrivergetcase.resultsdata:
            #print "******************"
            #print item["casename"]
            if(case["casename"]==item["casename"]):
                print item["casename"],item["casedataNo"]
                suite.addTest(Testdriver(item["casename"]+'__'+str(i)+'__'+username+'_'+str(item["casedataNo"])))
                i+=1
        i=1
    
    filename="../reporter/"+str(localtimes)+"_testReporter_"+username+".html"  #定义个报告存放路径，支持相对路径。
    fp=file(filename,'wb')
    runner = lib.HTMLTestRunner.HTMLTestRunner(stream=fp,title='API_test_'+str(localtimes),description='Report_description')  #使用HTMLTestRunner配置参数，输出报告路径、报告标题、描述
    runner.run(suite) #自动进行测试
    

if __name__ == '__main__':
    htr("tester")
    #htr("huohui")
    #htr("admin")

