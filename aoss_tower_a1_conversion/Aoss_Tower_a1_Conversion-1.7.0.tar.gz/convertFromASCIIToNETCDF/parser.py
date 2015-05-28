"""
The purpose of this class is to parse l00 
data into a dictionary. Its super class will inherit
these methods and use them to transer a 
dictionary of data into a netcdf file
"""

from aosstower.l00 import parser
import numpy as np
import abc
from Util import Util as u

class AossTowerParse(object):

    def __init__(self, date):
        self.Util = u()
        self.FILENAME = self.Util.FILENAME(date)

    # The purpose of this  function is to 
    # update the data dictionary
    #
    # @param out of date dictionary of data, the frame the parser is on
    # and a counter which is used to tell the frame's number
    # Handles missing data by filling in the numpy with -999.f
    #
    # @return updated dictionary of data
    def saveData(self, storeData, frame, counter):
	
        #save parameters
        #counter var
        c = counter
		
        #dict frame
        f = frame

        #store Dictionary obj
        s = storeData
		
        #for each key inside the dict of data
        #this loop will add a new value to the data's numpy
        #array
        for key in s:
			
            #this method will not handle stamp
            #stamp is handled in another method
            if key == 'stamp':
                continue		

            #gets old numpy array
            dataNumpy = s[key]
			
            #updates numpy array
            try:
                dataNumpy[counter] = f[key]

            #error means no data was found
            #so a fill value of -999.f is created
            except(KeyError):
                dataNumpy[counter] = float(-999)
			
            #updates the data
            s[key] = dataNumpy
		
        #returns the data	
        return s

    # the purpose of this function is to 
    # update a date time dictionary,
    # which holds all the stamp values
    #
    # @param the current frame, the frame's number, and 
    # an outdated date time dict
    #
    # @return updated date time dict
	
    def createStampDict(self, frame, counter, stampDict):
        #stamp dict
        sd = stampDict

        #retrieves stamp from the frame
        stamp = frame['stamp']
		
        #updates stamp dict
        sd[counter] = stamp

    # The purpose of this function 
    # is to calculate the number of iterations
    # needed for the length of numpies
    #
    # @param the filename the program parses
    #
    # @return the total number of frames for that file
    
    def calcNumItr(self):
        returnCounter = 0

        #update the counter
        for frame in parser.read_frames(self.FILENAME):
            returnCounter = returnCounter + 1

        #return the total number of iterations
        return returnCounter

    # no parameters
    # The purpose of this function is to
    # parse all frames into a huge set of frames
    #
    # @return huge set of frames

    def storeValues(self):

        #calculate total amount of frames
        numItr = self.calcNumItr()
		
        #create the dic of data
        storeData = {}

        for key in parser.database:
            storeData[key] = np.arange(numItr, dtype = 'float32')

        #create new stamp dic
        stampDict = {}

        #create counter
        counter  = 0

        #for every frame, store data and stamp
        for frame in parser.read_frames(self.FILENAME):
            storeData = self.saveData(storeData, frame, counter)
			
            self.createStampDict(frame, counter, stampDict)
			
            #increment counter so it can traverse and fill numpy arrays
            counter = counter + 1
		
        #tack stamp dict into the store data numpy
        storeData["stamp"] = stampDict
		
        #return the whole lot of data
        return storeData

