import unittest
from ATW import AossTowerWrite as ATW
from ATP import AossTowerParse as ATP
from aosstower.l00 import parser
import numpy as np
from random import randint as ri
from netCDF4 import Dataset
from datetime import datetime as dt
import platform
import os
import glob
import shutil
from Util import Util

class TestWrite(unittest.TestCase):

    # The purpose of this method is to set up the class
    # no parameters or returns

    @classmethod
    def setUpClass(cls):
        cls.createFiles = {}

        cls.createFiles[1] = ATW(ATP(dt(2003, 05, 28, 0, 0, 0)).storeValues(),
        dt(2003, 05, 28, 0, 0, 0))
        cls.createFiles[2] = ATW(ATP(dt(2003, 07, 27, 0, 0, 0)).storeValues(),
        dt(2003, 07, 27, 0, 0, 0))

        #write file
        for file in cls.createFiles:
            cls.createFiles[file].write()

        #read files for test
        cls.read = {}

        cls.read[1] = Dataset('rig-tower.2003-05-28.nc', 'r')
        cls.read[2] = Dataset('rig-tower.2003-07-27.nc', 'r')
        
    # The purpose of this f(x) is to see if the dimensions were written correctly
    # no parameters or returns

    def testWriteDim(self):
            #tests first date's  dimension properties
            self.assertEqual(256, len(self.read[1].dimensions['strlen']), 
            'size of strlen should be 256')

            self.assertEqual('strlen', self.read[1].dimensions['strlen'].name, 
            'the name of dimension should be strlen')

            sizeOfTime = 2511

            self.assertEqual('time', self.read[1].dimensions['time'].name,
            'the name of dimension should be time')

            self.assertEqual(sizeOfTime, len(self.read[1].dimensions['time']),
                'size of time should be the same as size of file')

            #tests empty ascii file dimensions
            self.assertEqual(256, len(self.read[2].dimensions['strlen']),   
            'size of strlen should be 256')

            self.assertEqual('strlen', self.read[2].dimensions['strlen'].name,   
            'the name of dimension should be strlen')

            sizeOfTime = 1

            self.assertEqual('time', self.read[2].dimensions['time'].name,
            'the name of dimension should be time')

            self.assertEqual(sizeOfTime, len(self.read[2].dimensions['time']),
                'size of time should be the same as size of file')

    def testAttributes(self):
        #all files have same attributes, so
        #for each file, test to see if attributes are the same
        for file in self.read:

            #tests to see if attributes match parser.database description
            getVars = self.read[file].variables

            #test vars in parser.database
            for key in parser.database:
                self.assertEqual(getVars[key].standard_name, 
                parser.database[key][1], 
                "standard name should match the one in database")

                self.assertEqual(getVars[key].description,
                parser.database[key][3], 
                "description should match the one in the database")

                self.assertEqual(getVars[key].units, parser.database[key][4],
                "units should match the units in the database")

                self.assertEqual(getVars[key]._FillValue, float(-999),
                "fill value should be -999.f")

                self.assertTrue(getVars[key].dimensions[0] == 'time', 
                "var should depend on time")

                self.assertTrue(len(getVars[key].dimensions) == 1, 
                "var should only depend on 1 dimension")

                self.assertTrue(getVars[key].dtype == np.float32, 
                "data type should be f32")
            
            #test other vars
            lon = getVars['lon']

            self.assertEqual(lon._FillValue, float(-999), 
            "fill value should be -999.f")
 
            self.assertEqual(lon.standard_name, "longitude", 
            "standard name for lon should be longitude")

            self.assertEqual(lon.valid_min, "-180L", "valid min for lon should be -180L")
            
            self.assertEqual(lon.units, "degrees_east", 
            "lon's units should be degrees_east")

            self.assertEqual(lon.valid_max, "180L", "valid max for lon should be 180L")

            self.assertTrue(len(lon.dimensions) == 0, "lon should depend on nothing")

            self.assertTrue(lon.dtype == np.float32, 
            "data type for lon should be f32")
 
            #test lat
            lat = getVars['lat']
            
            self.assertEqual(lat._FillValue, float(-999),
            "fill value should be -999.f")
   
            self.assertEqual(lat.valid_min, "-90L", "valid min for lat should be -90L")
            
            self.assertEqual(lat.standard_name, "latitude", 
            "standard name for lat should be latitude")

            self.assertEqual(lat.units, "degrees_north", 
            "the units for lat should be degrees north")

            self.assertEqual(lat.valid_max, "90L", "valid max for lat should be 90L")

            self.assertTrue(len(lat.dimensions) == 0, "lat should depend on nothing")

            self.assertTrue(lat.dtype == np.float32, "lat's data type should be f32")

            #test station name
            station_name = getVars['station_name']

            self.assertEqual(station_name._FillValue, '-',
            "station name's fill value should be \'-\'")

            self.assertEqual(station_name.long_name, "station name", 
            "station name's long name should be station name")

            self.assertEqual(station_name.cf_role, "timeseries_id",
            "station name's cf role should be timeseries id")

            self.assertTrue(station_name.dimensions[0] == 'strlen', 'station_name should depend on strlen')

            self.assertTrue(len(station_name.dimensions) == 1, 
            "station_name should depend only on strlen")

            self.assertTrue(station_name.dtype == 'S1', 
            "station name's type should be char")

            #test alt
            alt = getVars['alt']

            self.assertEqual(alt._FillValue, float(-999),
            "alt's fill value should be -999.f")

            self.assertEqual(alt.positive, "up", "alt's \'positive\' should be up")

            self.assertEqual(alt.long_name, "vertical distance", 
            "alt's long name should be vertical distance")
    
            self.assertEqual(alt.standard_name, "height",
            "alt's standard name should be height")

            self.assertEqual(alt.units,  "m", "alt's units should be m")
            
            self.assertEqual(alt.axis, "Z", "alt's axis should be the Z-axis")

            self.assertTrue(len(alt.dimensions) == 0, 
            "alt should depend on nothing")

            self.assertTrue(alt.dtype == 'float32',
            "alt's type should be f")

            #test base_time
            base_time = getVars['base_time']

            self.assertEqual(base_time._FillValue, float(-999),
            "base time's fill value should be -999.f")

            self.assertEqual(base_time.long_name, "base time as unix timestamp",
            "base_time's long name should be base time as unix timestamp")

            self.assertEqual(base_time.standard_name, "time",
            "base_time's standard name should be time")

            self.assertEqual(base_time.units,  
            "seconds since 1970-01-01 00:00:00 0:00", 
            "base_time's units should be seconds since 1970-01-01 00:00:00 0:00")

            if file == 1:
                date = "2003-05-28"

                self.assertEqual(base_time.string, 
                "2003-05-28 00:00:00Z", 
                "base_time's string should be date + 00:00:00Z")

            else:
                date = "2003-07-27"

                self.assertEqual(base_time.string,
                 "2003-07-27 00:00:00Z",                       
                "base_time's string should be date + 00:00:00Z")

            self.assertTrue(len(base_time.dimensions) == 0, 
            "base_time should depend on nothing")

            self.assertTrue(base_time.dtype == 'float32',
            "base_time's type should be f")

            #test time
            time = getVars['time']
            
            self.assertEqual(time._FillValue, float(-999),
            "time's fill value should be -999.f")

            self.assertEqual(time.long_name, "time offset from midnight UTC",
            "time's long name should be time offset from midnight UTC")

            self.assertEqual(time.standard_name, "time",
            "time's standard name should be time")

            self.assertEqual(time.units,  
            "seconds since " + date + " 00:00:00Z",
            "time's units should be seconds since current file's date 00:00:00Z")

            self.assertTrue(len(time.dimensions) == 1,
            "time should depend only on time")
            
            self.assertTrue(time.dimensions[0] == 'time', "time should depend on time")

            self.assertTrue(time.dtype == 'float32',
            "time's type should be f")

            #test global attributes
            self.assertEqual(self.read[file].source, 'surface observation',
            'global attribute souce should be surface observation')
    
            self.assertEqual(self.read[file].conventions, 'CF-1.6',
            'global attribute conventions should be CF-1.6')
 
            self.assertEqual(self.read[file].institution, 'UW SSEC',
            'global attribute institution should be UW SSEC')
 
            self.assertEqual(self.read[file].featureType, 'timeSeries', 
            'global attribute featureType should be timeSeries')

            uname = ' '.join(platform.uname()) + " ATW.pyc"

            self.assertTrue(self.read[file].history == uname,
            'global attribute history should be the uname plus script name')

    # The purpose of this method is to make sure the variables
    # were written correctly

    def testWriteVars(self):
        myUtil = Util()

        for key in parser.database:
            counter = 0

            #get actual values
            keyVals = self.read[1].variables[key][:]
                
            #get expected
            for frame in parser.read_frames(myUtil.FILENAME(dt(2003, 
            05, 28, 0, 0, 0))):

                try:
                    frame[key]
                    
                except(KeyError):
                    frame[key] = float(-999)
                    keyVals = self.read[1].variables[key][:].data[:]

                #compare actual and expected
                self.assertEqual(keyVals[counter], frame[key],
                "actual value should match expected")

                #inc counter
                counter += 1

        for key in parser.database:
            counter = 0

            #get actual values
            keyVals = self.read[2].variables[key][:]

            #compare actual and expected
            self.assertEqual(keyVals.data[counter], float(-999),
            "actual value should match expected")

        self.cleanup()

    def cleanup(self):
        filelist = glob.glob("*.nc")
        for file in filelist:
            os.remove(file)    

if __name__ == '__main__':
        unittest.main()
