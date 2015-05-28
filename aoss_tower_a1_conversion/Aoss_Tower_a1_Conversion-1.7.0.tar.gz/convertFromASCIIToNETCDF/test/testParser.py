import unittest
from aosstower.l00 import parser
from ATP import AossTowerParse
import numpy as np
from datetime import datetime
from random import randint as ri
import glob
from os import remove as rm

class TestParser(unittest.TestCase):

    # The purpose of this method is to set up the class for tests
    # no params
    # no returns

    @classmethod
    def setUpClass(cls):
	#two special cases
        #one where ascii file is empty
        #second case is the start of the day, 05-28-2003

        #normal case, every year

        cls.testDict = {}
        cls.testDict[1] = AossTowerParse(datetime(2003, 05, 28, 0, 0, 0))
        cls.testDict[2] = AossTowerParse(datetime(2003, 07, 27, 0, 0, 0))

    # The purpose of this function is to test the number
    # of iterations function in parser
    # no parameters or returns
        
    def test_Calculate_Number_Of_Iterations_Function(self):
        #in special cases, the number of frames are known
        #sees if calculations are correct		
        self.assertEqual(2511, 
        self.testDict[1].calcNumItr(), 
        "first test should return 2511 frames")
        
        #second special case
        self.assertEqual(0, 
        self.testDict[2].calcNumItr(), 
        "second test should return 0 frames")

    # tests to see if dict can append data correctly
    # no params or returns
	
    def test_Save_Data(self):
        expectedDict = {}		
        actualDict = {}

        #create numpy array
        for key in parser.database:
            expectedDict[key] = np.arange(4)
            actualDict[key] = np.arange(4)

        filename = '/mnt/inst-data/aoss-tower/2003/05/rig_tower.2003-05-28.ascii'

        #get last frame
        for frame in parser.read_frames(filename):
	        pass

        #add frame to expected
        for key in expectedDict:
	        try:
		        expectedDict[key][0] = frame[key]

	        except(KeyError):
		        expectedDict[key][0] = float(-999)

        #add frame to actual
        actualDict = self.testDict[1].saveData(actualDict, frame, 0)

        #new file
        filename = '/mnt/inst-data/aoss-tower/2009/05/rig_tower.2009-05-28.ascii'

        # get last frame
        for frame in parser.read_frames(filename):
            pass

        #appends to expected
        for key in expectedDict:
            try:
                expectedDict[key][1] = frame[key]

            except(KeyError):
                expectedDict[key][1] = float(-999)

        #adds to actual
        actualDict = self.testDict[1].saveData(actualDict, frame, 1)
		
        #new file	
        filename = '/mnt/inst-data/aoss-tower/2003/07/rig_tower.2003-07-27.ascii'

        #gets last frame
        for frame in parser.read_frames(filename):
                        pass

        #appends to expected
        for key in expectedDict:
            try:
                expectedDict[key][2] = frame[key]

            except(KeyError):
                expectedDict[key][2] = float(-999)


        #adds to actual
        actualDict = self.testDict[1].saveData(actualDict, frame, 2)

        #new file
        filename = '/mnt/inst-data/aoss-tower/2014/04/rig_tower.2014-04-01.ascii'

        #gets last frame
        for frame in parser.read_frames(filename):
            pass

        #adds to expected
        for key in expectedDict:
            try:
                expectedDict[key][3] = frame[key]

            except(KeyError):
                expectedDict[key][3] = float(-999)

        #appends to actual
        actualDict = self.testDict[1].saveData(actualDict, frame, 3)

        #tests to see if the frames appended as expected
        for key in expectedDict:
            self.assertIsNone(np.testing.assert_almost_equal(expectedDict[key], 
            actualDict[key]))

    # tests to see if stamps append as expected
    # no params or returns
    def test_Create_Stamp_Dictionary(self):
        expected = {}
        actual = {}

        filename = '/mnt/inst-data/aoss-tower/2003/05/rig_tower.2003-05-28.ascii'

        randomFrame = {}

        #chooses random frame
	randInt = ri(0, 2511)

        counter = 0

        #gets random frame
        for frame in parser.read_frames(filename):
            #When equal, frame retrieved
            if(counter == randInt):
                randomFrame = frame
 
            else:
                counter += 1

        #appends frame
        expected[0] = randomFrame['stamp']

        #appends to actual
        self.testDict[1].createStampDict(randomFrame, 0, actual)

        #test to see if frame was appended
        self.assertEqual(expected, actual, 
        "Dict should contain first random stamp")

        #chooses another random frame
        randInt = ri(0, 17280)

        counter = 0

        filename = '/mnt/inst-data/aoss-tower/2009/05/rig_tower.2009-05-28.ascii'
        
        #gets random frame
        for frame in parser.read_frames(filename):

            #when equal, retrieves frame
            if(counter == randInt):
                randomFrame = frame

            else:
                counter += 1

        #append frame to expected
        expected[1] = randomFrame['stamp']
        
        #trys to append to actual
        self.testDict[1].createStampDict(randomFrame, 1, actual) 

        #tests to see if frame actually appended 
        self.assertEqual(expected, actual, "Dict should contain second random stamp")

        filename = '/mnt/inst-data/aoss-tower/2014/04/rig_tower.2014-04-01.ascii'

        #gets another random frane
        randInt = ri(0, 17280)

        #gets random frame
        for frame in parser.read_frames(filename):
            #when equal, retrieves frame
            if(counter == randInt):
                randomFrame = frame

            else:
                counter += 1

        #appends to expected
        expected[2] = randomFrame['stamp']

        #trys to append to actual
        self.testDict[1].createStampDict(randomFrame, 2, actual)

        #tests if they are equal
        self.assertEqual(expected, actual, "Dict should contain third random stamp")

    # The purpose of this function is to test if the values are
    # being stored correctly
    # no parameters or returns

    def test_Store_Values(self):
        #stores values for first test
        actual = self.testDict[1].storeValues()

        testOneFilename = '/mnt/inst-data/aoss-tower/2003/05/rig_tower.2003-05-28.ascii'

        #tests if the results are what they should be
        for key in parser.database:
            counter = 0

            #parses through ascii file
            #checks to see if each value in a frame is equal
            for frame in parser.read_frames(testOneFilename):
                #gets key's value in a frame
		try:
			frame[key]
                #fills in value if needbe
                except KeyError:
                        frame[key] = float(-999)

                #tests if the frame's value is equal to actual value
                self.assertEqual(frame[key], actual[key][counter], 
                "first test's frame value based upon key should equal actual value")
                counter += 1	
        
        #tests if results are what they should be for each file
        for key in self.testDict:
            actual = self.testDict[key].storeValues()

            #gets an actual key from database
            for frameKey in parser.database:
            
                counter = 0

                #runs key through every frame
                for frame in parser.read_frames(self.testDict[key].FILENAME):
                  
                    #gets value
                    try:
                            frame[frameKey]

                    #uses fillvalue if needbe
                    except KeyError:
                            frame[frameKey] = float(-999)

                    #makes sure expected is same as actual
                    self.assertEqual(frame[frameKey], actual[frameKey][counter], 
                    "regular test's frame value based upon key should equal actual value")
                    counter += 1

        #tests special case two
        actual = self.testDict[2].storeValues()
        
        #tests to see if each numpy array is empty
        for key in parser.database:
            self.assertTrue(not actual[key], "third test should return empty numpys")

        #cleans up the nc files
        self.cleanup()

    # The purpose of this function is to remove all the nc files
    # no params
    # no returns
    def cleanup(self):
        filelist = glob.glob("*.nc")
        for file in filelist:
            rm(file)

if __name__ == '__main__':
	unittest.main()
