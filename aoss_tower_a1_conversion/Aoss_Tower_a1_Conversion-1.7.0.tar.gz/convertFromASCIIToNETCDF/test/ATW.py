"""
The purpose of this class is to take the created dict of data from parse
and transfer that into a netcdf4 file
the data is all based on the date the user enters
and stored in a file that the user enters
"""

from  netCDF4 import Dataset
import numpy as np
from ATP import AossTowerParse as parser
from aosstower.l00 import parser as atParser
from Util import Util as u
import sys
import shutil
import os
import errno
from datetime import datetime as dt
from aosstower import station as stion
import platform

class AossTowerWrite(object):
	
    # The purpose of this function is to use date
    # to get path and create file
    # also initializes values
    # takes parser as a parameter

    def __init__(self, dictData, date):
        self.Util = u()
        
        self.dictData = dictData

        if(len(self.dictData['stamp']) > 0):
            self.date = self.dictData['stamp'][1]

        else:
            self.date = date

        self.ncFileName = self.Util.ncFileName(self.date)
 
        self.ncFile = Dataset(self.ncFileName, 'w')
	
    # The purpose of this function is to write the dimensions
    # for the nc file
    # no parameters
    # no returns

    def writeDim(self):
        #creates dimensions
        self.ncFile.createDimension('time', len(self.dictData['stamp']))
        self.ncFile.createDimension('strlen', 256)

    # The purpose of this function is to write variable atrributes to the file
    # no parameters
    # returns whether or not the ascii file was empty or not
    # if it was, then the netcdf file is corrupted

    def writeVarAttributes(self):
		
        database = atParser.database

        #create coordinate var lon
        lon = self.ncFile.createVariable('lon', np.float32, 
        fill_value = float(-999))
        lon.valid_min = '-180L'
        lon.standard_name = 'longitude'
        lon.units = 'degrees_east'
        lon.valid_max = '180L'

        #create coordinate var lat
        lat = self.ncFile.createVariable('lat', np.float32,
        fill_value = float(-999))
        lat.valid_min = '-90L'
        lat.standard_name = 'latitude'
        lat.units = 'degrees_north'
        lat.valid_max = '90L'

        #create var dependent on strlen
        stationName = self.ncFile.createVariable('station_name',
        'c', dimensions=('strlen'), fill_value = "-")
        stationName.long_name = 'station name'
        stationName.cf_role = 'timeseries_id'

        #create coordinate var alt
        alt = self.ncFile.createVariable('alt', np.float32,
        fill_value = float(-999))
        alt.positive = 'up'
        alt.long_name = 'vertical distance'
        alt.standard_name = 'height'
        alt.units = 'm'
        alt.axis = 'Z'

        #create base_time
        baseTime = self.ncFile.createVariable('base_time', np.float32,
        fill_value = float(-999))
        baseTime.long_name = 'base time as unix timestamp'
        baseTime.standard_name = 'time'
        baseTime.units = 'seconds since 1970-01-01 00:00:00 0:00'
        baseTime.string = self.Util.dateFormat(self.date) + ' 00:00:00Z'

        #create time
        time = self.ncFile.createVariable('time', 
        np.float32,dimensions = ('time'), fill_value = float(-999))
        time.long_name = 'time offset from midnight UTC'
        time.standard_name = 'time'
        Z = ' 00:00:00Z'
        time.units = 'seconds since ' + self.Util.dateFormat(self.date) + Z

        #creates variable for each key in the database
        #uses database's information
        for key in database:
            if key == 'stamp':
                continue
			
            var = database[key]

            printString = self.ncFile.createVariable(key, np.float32,
            dimensions=('time'), fill_value = float(-999))
            printString.standard_name = var[1]
            printString.description = var[3]
            printString.units = var[4]
		
        #create global attributes
        #these might change
        self.ncFile.source = 'surface observation'
        self.ncFile.conventions = 'CF-1.6'
        self.ncFile.institution = 'UW SSEC'
        self.ncFile.featureType = 'timeSeries'

        #generate history
        self.ncFile.history = ' '.join(platform.uname()) + " " + os.path.basename(__file__)
	
    # The purpose of this function is to write
    # in the fill values for an empty ascii file
    # fills all data variables with -999.f
    #no parameters or returns
    def fillValues(self):
        year = self.date.year
        month = self.date.month
        day = self.date.day

        #creates new datetime at start of day
        baseTimeValue = dt(year, month, day)
		
        #find out how much time 
        #elapsed since the start of the day,
        #to the first time stamp
        baseTimeValue = baseTimeValue - baseTimeValue.fromtimestamp(0)

        #calculates the total seconds of that difference
        baseTimeValue = baseTimeValue.total_seconds()

        fileVar = self.ncFile.variables

        fileVar['lon'].assignValue(stion.LONGITUDE)
        fileVar['lat'].assignValue(stion.LATITUDE)
        fileVar['alt'].assignValue(self.Util.ALTITUDE())

        #this name might change later
        stationsName = ("AOSS Tower")

        #transfers string to numpy array of type S1
        #same type as the var station name
        arrayOfChars = list(stationsName)
        toNumpy = np.asarray(arrayOfChars)

         #writes station name to file    
        fileVar['station_name'][0:len(toNumpy)] = toNumpy

        #writes data into file
        for key in atParser.database:

            #fills in numbers
            inFileVar = fileVar[key]
            inFileVar[0] = float(-999)

        #writes in base time and time
        inFileVar = fileVar['base_time']
        inFileVar.assignValue(baseTimeValue)

        inFileVar = fileVar['time']
        inFileVar[0] = float(-999)

    # The purpose of this function is to take the data
    # from a full ascii file and write it into the netcdf file
    # @param the big dictionary of data
    # no returns

    def writeData(self):
        #gets dict of date time objects
        stamp = self.dictData['stamp']

        # create new stamp numpy
        timeNumpy = np.empty(len(stamp), dtype = 'float32')

        #get date time object
        baseTimeValue = dt(stamp[0].year, stamp[0].month, stamp[0].day)

        #find out how much time 
        #elapsed since the start of the day,
        #to the first time stamp
        baseTimeValue = baseTimeValue - baseTimeValue.fromtimestamp(0)

        #calculates the total seconds of that difference
        baseTimeValue = baseTimeValue.total_seconds()

        #keep track of the frame number
        counter = 0

        #for each frame number
        #calculates how much time has elapsed since base time
        #stores that value in time numpy
        for key in stamp:
                timeValue = stamp[key] - dt(stamp[0].year, stamp[0].month, stamp[0].day)
                timeValue = timeValue.total_seconds()

                timeNumpy[counter] = timeValue
                counter = counter + 1

        fileVar = self.ncFile.variables

        #write corrdinate variable values to file
        fileVar['lon'].assignValue(stion.LONGITUDE)
        fileVar['lat'].assignValue(stion.LATITUDE)
        fileVar['alt'].assignValue(self.Util.ALTITUDE())
 
        #this name might change later
        stationsName = ("AOSS Tower")

        #transfers string to numpy array of type S1
        #same type as the var station name
        arrayOfChars = list(stationsName)
        toNumpy = np.asarray(arrayOfChars)

         #writes station name to file    
        fileVar['station_name'][0:len(toNumpy)] = toNumpy

        #writes data into file
        for key in self.dictData:
                
            #writes in base time and time
            if key == 'stamp':
                inFileVar = fileVar['base_time']
                inFileVar.assignValue(baseTimeValue)

                inFileVar = fileVar['time']
                inFileVar[:] = timeNumpy

                continue

            inFileVar = fileVar[key]
            inFileVar[:] = self.dictData[key]

    # The purpose of this function is to write all data into an nc file
    # no parameters
    # no returns

    def write(self):
        self.writeDim()
        self.writeVarAttributes()
        
        if(not self.dictData['stamp']):
            self.fillValues()

        else:
            self.writeData()

        #tell user data succeeded
        print "data written succesfully"

        #closes file
        self.ncFile.close()
