__author__ = 'AssadMahmood'
import unittest
import asposecloud
import os.path
import json

from asposecloud.storage import Folder
from asposecloud.imaging import Document
from asposecloud.imaging import Image


class TestAsposeImaging(unittest.TestCase):

    def setUp(self):
        with open('setup.json') as json_file:
            data = json.load(json_file)

        asposecloud.AsposeApp.app_key = str(data['app_key'])
        asposecloud.AsposeApp.app_sid = str(data['app_sid'])
        asposecloud.AsposeApp.output_path = str(data['output_location'])
        asposecloud.Product.product_uri = str(data['product_uri'])

    def test_update_tiff_properties(self):
        folder = Folder()
        response = folder.upload_file('./data/barcodeQR.tiff')
        self.assertEqual(True, response)

        doc = Document('barcodeQR.tiff')
        response = doc.update_tiff_properties(1,'ccittfax3','inch',300,300,96,96,'')
        self.assertTrue(os.path.exists(response))

    def test_update_tiff_properties_local(self):
        doc = Document('barcodeQR.tiff')
        response = doc.update_tiff_properties_local('./data/barcodeQR.tiff',1,'ccittfax3','inch',300,300,96,96,'')
        self.assertTrue(os.path.exists(response))

    def test_crop_image(self):
        folder = Folder()
        response = folder.upload_file('./data/barcodeQR.jpg')
        self.assertEqual(True, response)

        img = Image('barcodeQR.jpg')
        response = img.crop_image(0,0,10,10,'/','jpg')
        self.assertTrue(os.path.exists(response))

    def test_append_tiff(self):
        folder = Folder()
        response = folder.upload_file('./data/barcodeQR.tiff')
        self.assertEqual(True, response)

        folder = Folder()
        response = folder.upload_file('./data/test_convert_cell.tiff')
        self.assertEqual(True, response)

        doc = Document('barcodeQR.tiff')
        response = doc.append_tiff('test_convert_cell.tiff')
        self.assertEqual(dict, type(response))

    def test_update_image(self):
        folder = Folder()
        response = folder.upload_file('./data/barcodeQR.jpg')
        self.assertEqual(True, response)

        img = Image('barcodeQR.jpg')
        response = img.update_image({'newWidth': 20, 'newHeight': 20},'jpg')
        self.assertTrue(os.path.exists(response))

    def test_get_tiff_frame_properties(self):
        folder = Folder()
        response = folder.upload_file('./data/sample.tif')
        self.assertEqual(True, response)

        doc = Document('sample.tif')
        response = doc.get_tiff_frame_properties(0)
        self.assertEqual(dict, type(response))

    def test_extract_frame(self):
        folder = Folder()
        response = folder.upload_file('./data/sample.tif')
        self.assertEqual(True, response)

        doc = Document('sample.tif')
        response = doc.extract_frame(0)
        self.assertTrue(os.path.exists(response))

    def test_resize_tiff_frame(self):
        folder = Folder()
        response = folder.upload_file('./data/sample.tif')
        self.assertEqual(True, response)

        img = Image('sample.tif')
        response = img.resize_tiff_frame(0,100,100,'/')
        self.assertTrue(os.path.exists(response))

    def test_crop_tiff_frame(self):
        folder = Folder()
        response = folder.upload_file('./data/sample.tif')
        self.assertEqual(True, response)

        img = Image('sample.tif')
        response = img.crop_tiff_frame(0,0,0,100,100,'/')
        self.assertTrue(os.path.exists(response))

    def test_rotate_tiff_frame(self):
        folder = Folder()
        response = folder.upload_file('./data/sample.tif')
        self.assertEqual(True, response)

        img = Image('sample.tif')
        response = img.rotate_tiff_frame(0,'rotate90flipnone','/')
        self.assertTrue(os.path.exists(response))

    def test_update_tiff_frame(self):
        folder = Folder()
        response = folder.upload_file('./data/sample.tif')
        self.assertEqual(True, response)

        img = Image('sample.tif')
        response = img.update_tiff_frame(0,{'newWidth':10,'newHeight':10})
        self.assertTrue(os.path.exists(response))


if __name__ == '__main__':
    unittest.main()