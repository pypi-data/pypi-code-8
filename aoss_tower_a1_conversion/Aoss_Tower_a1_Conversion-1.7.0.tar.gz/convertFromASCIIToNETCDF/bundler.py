"""
The purpose of this module is to use 
recursion to continuously prompt the user
for file names and data dates
"""

from parser import AossTowerParse
from WriteToNetCDF import AossTowerWrite as ATW

from Util import Util
from datetime import datetime as date
from datetime import timedelta as delta
import os
import shutil

# The purpose of this function is to move the newly
# created file.
# Also moves the file into directories based upon
# the file's date
# @param path
# no returns

def moveFile(writer):
    #get path
    myUtil = Util()

    path = myUtil.destinationPath(writer.date)

    #if the path does not exist, create it
    if(not os.path.exists(path)):
        print "creating path..."
        os.makedirs(path)
        print "path created"

    #notify user
    print "path loaded"

    #moves file
    shutil.move(writer.ncFileName, path + writer.ncFileName)
    print "file moved"

# The purpose of this function is to write data based upon
# a start or end date, then move folders based upon
# a user given path
# @param starting datetime obj, ending datetime obj, path
# no return

#has some sort of bug. File Not Found exception was thrown
def writeRange(startDate, endDate):
    #holds the current date time in the loop
    cur_dt = startDate

    #for each day in the range, write
    #a netcdf file
    for day in range((endDate - startDate).days + 1):

        #writes to file
        myParser = AossTowerParse(cur_dt)
        dictData = myParser.storeValues()
        writer = ATW(dictData, cur_dt)
        writer.write()
        moveFile(writer)

        #forwards current datetime by a day
        cur_dt += delta(days = 1)

# The purpose of this function is to get the user to input
# a start and end date and convert all ascii files to netcdf files based
# within that range
# no parameters
# no returns

# The purpose of this function is to convert
# all ascii files into netcdf files
# runs for as long as memory holds
# no paramters or returns

def all():
    writeRange(date(2003, 5, 28,  20, 30, 46), date.today())

# The purpose of this function is to take yesterday's
# ascii file and convert it to netcdf

def convertYesterdayFile():
    
    myUtil = Util()
    yesterdaysDate = myUtil.getYesterdaysDTobj()
    myParser = AossTowerParse(yesterdaysDate)
    dictData = myParser.storeValues()
    myWriter = ATW(dictData, yesterdaysDate)
    myWriter.write()
    moveFile(myWriter)

#writeRange(date(2003,5,28,20,30,46), date(2003,7,15,0,0,0))
#writeRange(date(2003,7,27,0,0,0), date(2003,7,27,0,0,0))
#all()
