__author__ = 'AssadMahmood'
import unittest
import asposecloud
import os.path
import json

from asposecloud.storage import Folder
from asposecloud.email import Document


class TestAsposeImaging(unittest.TestCase):

    def setUp(self):
        with open('setup.json') as json_file:
            data = json.load(json_file)

        asposecloud.AsposeApp.app_key = str(data['app_key'])
        asposecloud.AsposeApp.app_sid = str(data['app_sid'])
        asposecloud.AsposeApp.output_path = str(data['output_location'])
        asposecloud.Product.product_uri = str(data['product_uri'])

    def test_add_attachment(self):
        folder = Folder()
        response = folder.upload_file('./data/EmailTest.eml')
        self.assertEqual(True, response)

        folder = Folder()
        response = folder.upload_file('./data/sample.tif')
        self.assertEqual(True, response)

        doc = Document('EmailTest.eml')
        response = doc.add_attachment('sample.tif')
        self.assertEqual(dict, type(response))

if __name__ == '__main__':
    unittest.main()