from Util import Util
from datetime import datetime as dt
from datetime import timedelta as delta
import unittest

class TestUtil(unittest.TestCase):

    # The purpose of this method is to set up the class for tests
    # no params
    # no returns

    @classmethod
    def setUpClass(cls):
        cls.myUtil = Util()

    def date(self):
        return dt(2003,05,28,0,0,0)

    def cwd(self):
        return '/home/kgao/Code/Aoss_Tower_a1_Conversion/convertFromASCIIToNETCDF/test'


    # The purpose of this function is to test
    # Util's FILENAME function
    def test_FILENAME(self):
        start = self.date()
        expectedAsciiFilename = '/mnt/inst-data/aoss-tower/2003/05/rig_tower.2003-05-28.ascii'
        self.assertEqual(expectedAsciiFilename,
                   self.myUtil.FILENAME(start), "ascii filename format was wrong")
    
    def test_DestinationPath(self):
        start = self.date()
        expectedPath = self.cwd() + '/2003/2003-05/'
 
        self.assertEqual(expectedPath, 
                    self.myUtil.destinationPath(start), 'path format was wrong')

    def test_ncFileName(self):
        start = self.date()
        expectedNCFilename = 'rig-tower.2003-05-28.nc'
  
        self.assertEqual(expectedNCFilename, self.myUtil.ncFileName(start),
        'ncFileName format did not match')

    def test_Altitude(self):
        self.assertEqual(328, self.myUtil.ALTITUDE(), 'altitude should\'ve been 328')

    def test_DateFormat(self):
        start = self.date()
        expectedFormat = '2003-05-28'
      
        self.assertEqual(expectedFormat, self.myUtil.dateFormat(start),
                        'date format was wrong')

    def test_getYesterdaysDTobj(self):
        yesterday = dt(2015, 05, 20, 0, 0, 0)
        
        self.assertEqual(yesterday.year, self.myUtil.getYesterdaysDTobj().year,
                        'got unexpected year')
       
        self.assertEqual(yesterday.day, self.myUtil.getYesterdaysDTobj().day,
                        'got unexpected day')

        self.assertEqual(yesterday.month, self.myUtil.getYesterdaysDTobj().month,
                        'got unexpected month')
            
if __name__ == '__main__':
    unittest.main()
