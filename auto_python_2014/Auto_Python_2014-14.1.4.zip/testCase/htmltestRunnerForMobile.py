#coding=utf-8
import unittest
import lib.HTMLTestRunner
from testDataDriverForMobile import Testdriver
import time
import sys,os
from component.CPT_driver_cases import Drivergetcase

reload(sys)
sys.setdefaultencoding('utf-8')

def htr(username):
    tdrivergetcase=Drivergetcase()
    tdrivergetcase.cpt_setUsername(username)
    tdrivergetcase.cpt_createdbconnection()
    tdrivergetcase.cpt_getcases_mobile()
    #print "*********"
    #print tdrivergetcase.results

    tdrivergetcase.cpt_getcases_mobile_data()
    #print "*********"
    #print tdrivergetcase.resultsdata

    localtimes = time.strftime('%Y-%m-%d_%H-%M-%S',time.localtime(time.time()))
    suite=unittest.TestSuite()   #定义一个单元测试容器

    for case in tdrivergetcase.results:
        #print case
        i=1
        for item in tdrivergetcase.resultsdata:
            if(case==item["api"]):
                #print "******"
                #print item["api"],item["casesn"]
                suite.addTest(Testdriver(item["api"]+'__'+str(item["casesn"])))
                i+=1
        i=1
    
    #filename="../reporter/"+str(localtimes)+"_testReporter_"+username+".html"  #定义个报告存放路径，支持相对路径。
    filename="E:/DHTester/MobileAPI/"+str(localtimes)+"_testReporter_"+username+".html"  #定义个报告存放路径，支持相对路径。
    fp=file(filename,'wb')
    runner = lib.HTMLTestRunner.HTMLTestRunner(stream=fp,title='API_test_'+str(localtimes),description='Report_description')  #使用HTMLTestRunner配置参数，输出报告路径、报告标题、描述
    runner.run(suite) #自动进行测试
    

if __name__ == '__main__':
    htr("tester")
    #htr("huohui")
    #htr("admin")

