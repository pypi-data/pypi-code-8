#import testCase.htmltestRunnerForMobile
#testCase.htmltestRunnerForMobile.htr("tester")
import unittest
from testAutoCreateMethod import Testdriver

if __name__ == '__main__':
    suite=unittest.TestSuite()
    i=1
    while (i<3):
        testName="testdhnew_items_get__"+str(i)
        suite.addTest(Testdriver(testName))
        unittest.TextTestRunner(verbosity=2).run(suite)
        i=i+1
    #Testdriver().extends('testdhnew_items_get2',method_str)
    #suite.addTest(Testdriver("testdhnew_items_get2__1"))
    #unittest.TextTestRunner(verbosity=2).run(suite)