import unittest
from ATW import AossTowerWrite as ATW
from ATP import AossTowerParse as ATP
from aosstower.l00 import parser
from datetime import datetime as dt
import os
import glob
import shutil
from Util import Util
import bundler
from datetime import timedelta as delta

class TestWrite(unittest.TestCase):

    # The purpose of this method is to set up the class
    # no parameters or returns

    def test_move(self):
        parser = ATP(dt(2003, 05, 28, 0, 0, 0))
        
        dictData = parser.storeValues()
        
        writer = ATW(dictData, dt(2003, 05, 28, 0, 0, 0))

        bundler.moveFile(writer)

        currPath = os.getcwd()              #get current path

        os.chdir('2003')
        os.chdir('2003-05')

        #checks to see if file is there
        self.assertTrue(os.path.isfile('rig-tower.2003-05-28.nc'))

        #return to previous folder
        os.chdir(currPath)

        #removes all newly created directories
        for path in glob.glob("2*"):
            shutil.rmtree(path)

    def moved(self, date):
        currPath = os.getcwd()              #get current path

        myUtil = Util()

        dateFormat = myUtil.dateFormat(date)

        year = dateFormat[:4]

        monthYear = dateFormat[:7]

        os.chdir(year)
        os.chdir(monthYear)

        #checks to see if file is there
        self.assertTrue(os.path.isfile('rig-tower.' + dateFormat + '.nc'))

        #return to previous folder
        os.chdir(currPath)

    def test_Range(self):
        start = dt(2003, 05, 28, 0, 0, 0)
        end = dt(2004, 05, 28, 0, 0, 0)

        bundler.writeRange(start, end)

        currdt = start

        for day in range((start - end).days + 1):
            self.moved(curdt)
            curdt += delta(days = 1)

        #removes all newly created directories
        for path in glob.glob("2*"):
            shutil.rmtree(path)

    def test_Convert_Yesterday_File(self):
        bundler.convertYesterdayFile()
        yesterday = dt.today() - delta(1)

        self.moved(yesterday)

if __name__ == '__main__':
    unittest.main()

