from datetime import datetime
from datetime import timedelta

"""
This class takes dates and generates paths based upon those
date time objects.
"""

class Util(object):

    # the purpose of this function is to return 
    # the filename that the parser is going to use
    # based upon a datetime object
    # @param datetime object
    #
    # @return filename

    def FILENAME(self, date):
        month = date.month

        if(month < 10):
            month = "0" + (str)(month)
        else:
            month = (str)(month)

        day = date.day

        if(day < 10):
            day = "0" + (str)(day)
	
        else:
            day = (str)(day)

        #get total date
        totalDate = (str)(date.year) + "-" + month + "-" + day

        #returns file name
        return '/mnt/inst-data/aoss-tower/' + (str)(date.year) + '/' + month + '/rig_tower.' + totalDate + '.ascii'

    # create path based on the date
    # @return filepath
    # @param date

    def destinationPath(self, date):
        year = str(date.year)

        if date.month < 10:
            month = "0" + str(date.month)
       
        else:
            month = str(date.month)
        
        if(date.day < 10):
            day = "0" + str(date.day)

        else:
            day = str(date.day)

        #all file paths start with
        startofPath = "/data3/kgao/testAll15/"
        
        #next part of path is year + year-month
        eOPath = year + "/" + year + "-" + month + "/"

        return startofPath + eOPath

    # create netCDF4 file name
    # @return file name
    # @param date

    def ncFileName(self, date):
        year = str(date.year)

        if date.month < 10:
            month = "0" + str(date.month)

        else:
            month = str(date.month)

        if(date.day < 10):
            day = "0" + str(date.day)

        else:
            day = str(date.day)

        #create netCDF name
        netCDFName = "rig-tower." + year + "-" + month + "-" + day + ".nc"

        #returns newly created name
        return netCDFName

    # altitude value is not exact
    # return altitude value
    # @return altitude value
    # no parameters

    def ALTITUDE(self):
        return 328 

    # create a date format from datetime
    # @param datetime obj
    # @return YYYY-MM-DD

    def dateFormat(self, date):
        year = str(date.year)

        if date.month < 10:
            month = "0" + str(date.month)

        else:
            month = str(date.month)

        if(date.day < 10):
            day = "0" + str(date.day)

        else:
            day = str(date.day)

        #return YYYY-MM-DD
        return year + "-" + month + "-" + day

    # The purpose of this function is to generate yesterday's datetime
    # obj.
    # no parameters
    # @return yesterday's datetime object

    def getYesterdaysDTobj(self):
        #time difference of 1 day
        td = timedelta(1)

        return datetime.today() - td
