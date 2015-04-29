__author__ = 'AssadMahmood'
import unittest
import asposecloud
import os.path
import json

from asposecloud.storage import Folder
from asposecloud.tasks import Document
from asposecloud.tasks import Calendar



class TestAsposeImaging(unittest.TestCase):

    def setUp(self):
        with open('setup.json') as json_file:
            data = json.load(json_file)

        asposecloud.AsposeApp.app_key = str(data['app_key'])
        asposecloud.AsposeApp.app_sid = str(data['app_sid'])
        asposecloud.AsposeApp.output_path = str(data['output_location'])
        asposecloud.Product.product_uri = str(data['product_uri'])

    def test_add_link(self):
        folder = Folder()
        response = folder.upload_file('./data/test_tasks.mpp')
        self.assertEqual(True, response)

        link_data = {"Link":None,"Index":0,"PredecessorUid":1,"SuccessorUid":3,"LinkType":3,"Lag":9600,"LagFormat":4}

        doc = Document('test_tasks.mpp')
        response = doc.add_link(link_data)
        self.assertEqual(dict, type(response))

    def test_add_calendar(self):
        folder = Folder()
        response = folder.upload_file('./data/test_tasks.mpp')
        self.assertEqual(True, response)

        calendar_data = {"Name":"ADDED CALENDAR","Uid":0,"Days":[{"DayType":1,"DayWorking":False,
                                                                  "FromDate":"0001-01-01T00:00:00",
                                                                  "ToDate":"0001-01-01T00:00:00",
                                                                  "WorkingTimes":[]},
                                                                 {"DayType":2,"DayWorking":True,
                                                                  "FromDate":"0001-01-01T00:00:00",
                                                                  "ToDate":"0001-01-01T00:00:00",
                                                                  "WorkingTimes":[{"FromTime":"2010-01-01T09:00:00",
                                                                                   "ToTime":"2010-01-01T12:00:00"},
                                                                                  {"FromTime":"2010-01-01T13:00:00",
                                                                                   "ToTime":"2010-01-01T18:00:00"}]},
                                                                 {"DayType":3,"DayWorking":True,
                                                                  "FromDate":"0001-01-01T00:00:00",
                                                                  "ToDate":"0001-01-01T00:00:00",
                                                                  "WorkingTimes":[{"FromTime":"2010-01-01T09:00:00",
                                                                                   "ToTime":"2010-01-01T12:00:00"},
                                                                                  {"FromTime":"2010-01-01T13:00:00",
                                                                                   "ToTime":"2010-01-01T18:00:00"}]},
                                                                 {"DayType":4,"DayWorking":True,
                                                                  "FromDate":"0001-01-01T00:00:00",
                                                                  "ToDate":"0001-01-01T00:00:00",
                                                                  "WorkingTimes":[{"FromTime":"2010-01-01T09:00:00",
                                                                                   "ToTime":"2010-01-01T12:00:00"},
                                                                                  {"FromTime":"2010-01-01T13:00:00",
                                                                                   "ToTime":"2010-01-01T18:00:00"}]},
                                                                 {"DayType":5,"DayWorking":True,
                                                                  "FromDate":"0001-01-01T00:00:00",
                                                                  "ToDate":"0001-01-01T00:00:00",
                                                                  "WorkingTimes":[{"FromTime":"2010-01-01T09:00:00",
                                                                                   "ToTime":"2010-01-01T12:00:00"},
                                                                                  {"FromTime":"2010-01-01T13:00:00",
                                                                                   "ToTime":"2010-01-01T18:00:00"}]},
                                                                 {"DayType":6,"DayWorking":True,
                                                                  "FromDate":"0001-01-01T00:00:00",
                                                                  "ToDate":"0001-01-01T00:00:00",
                                                                  "WorkingTimes":[{"FromTime":"2010-01-01T09:00:00",
                                                                                   "ToTime":"2010-01-01T12:00:00"},
                                                                                  {"FromTime":"2010-01-01T13:00:00",
                                                                                   "ToTime":"2010-01-01T18:00:00"}]},
                                                                 {"DayType":7,"DayWorking":True,
                                                                  "FromDate":"0001-01-01T00:00:00",
                                                                  "ToDate":"0001-01-01T00:00:00",
                                                                  "WorkingTimes":[{"FromTime":"2010-01-01T09:00:00",
                                                                                   "ToTime":"2010-01-01T13:00:00"}]}],
                         "Exceptions":[],"IsBaseCalendar":True,"BaseCalendar":None,"IsBaselineCalendar":False}

        cal = Calendar('test_tasks.mpp')
        response = cal.add_calendar(calendar_data)
        self.assertEqual(dict, type(response))

if __name__ == '__main__':
    unittest.main()