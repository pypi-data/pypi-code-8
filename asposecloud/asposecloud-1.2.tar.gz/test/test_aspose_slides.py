__author__ = 'AssadMahmood'
import unittest
import asposecloud
import os.path
import json
import time

from asposecloud.storage import Folder
from asposecloud.slides import Converter
from asposecloud.slides import Document
from asposecloud.slides import Extractor

class TestAsposeSlides(unittest.TestCase):

    def setUp(self):
        with open('setup.json') as json_file:
            data = json.load(json_file)

        asposecloud.AsposeApp.app_key = str(data['app_key'])
        asposecloud.AsposeApp.app_sid = str(data['app_sid'])
        asposecloud.AsposeApp.output_path = str(data['output_location'])
        asposecloud.Product.product_uri = str(data['product_uri'])

    def test_create_empty_presentation(self):
        filename = str(time.time()) + '.pptx'
        doc = Document(filename)
        response = doc.create_empty_presentation()
        self.assertEqual(dict, type(response))

    def test_add_slide(self):
        filename = str(time.time()) + '.pptx'
        doc = Document(filename)
        response = doc.create_empty_presentation()
        self.assertEqual(dict, type(response))

        response = doc.add_slide(1)
        self.assertEqual(dict, type(response))

    def test_clone_slide(self):
        filename = str(time.time()) + '.pptx'
        doc = Document(filename)
        response = doc.create_empty_presentation()
        self.assertEqual(dict, type(response))

        response = doc.clone_slide(1,1)
        self.assertEqual(dict, type(response))

    def test_change_position(self):
        folder = Folder()
        response = folder.upload_file('./data/test_convert_slide.pptx')
        self.assertEqual(True, response)

        doc = Document('test_convert_slide.pptx')
        doc.add_slide(1)
        response = doc.change_slide_position(1,2)
        self.assertEqual(dict, type(response))

    def test_delete_all_slides(self):
        folder = Folder()
        response = folder.upload_file('./data/test_convert_slide.pptx')
        self.assertEqual(True, response)

        doc = Document('test_convert_slide.pptx')
        response = doc.delete_all_slides()
        self.assertEqual(dict, type(response))

    def test_merge_presentations(self):
        filename = str(time.time()) + '.ppt'
        doc = Document(filename)
        response = doc.create_empty_presentation()
        self.assertEqual(dict, type(response))

        filename1 = str(time.time()) + '1.ppt'
        doc = Document(filename1)
        response = doc.create_empty_presentation()
        self.assertEqual(dict, type(response))

        filename2 = str(time.time()) + '2.ppt'
        doc = Document(filename2)
        response = doc.create_empty_presentation()
        self.assertEqual(dict, type(response))

        merge_arr = {'List': [filename1,filename2]}
        doc = Document(filename)
        response = doc.merge_presentations(merge_arr)
        self.assertEqual(dict, type(response))

    def test_split_presentation(self):
        folder = Folder()
        response = folder.upload_file('./data/test_convert_slide.pptx')
        self.assertEqual(True, response)

        doc = Document('test_convert_slide.pptx')
        response = doc.split_presentation(1,1)
        self.assertEqual(dict, type(response))

    def test_get_background(self):
        folder = Folder()
        response = folder.upload_file('./data/test_convert_slide.pptx')
        self.assertEqual(True, response)

        doc = Document('test_convert_slide.pptx')
        response = doc.get_background(1)
        self.assertNotEquals(False, response)

    def test_get_all_text_items(self):
        folder = Folder()
        response = folder.upload_file('./data/test_convert_slide.pptx')
        self.assertEqual(True, response)

        doc = Document('test_convert_slide.pptx')
        response = doc.get_all_text_items()
        self.assertNotEquals(False, response)

    def test_get_comments(self):
        folder = Folder()
        response = folder.upload_file('./data/test_convert_slide.pptx')
        self.assertEqual(True, response)

        doc = Extractor('test_convert_slide.pptx')
        response = doc.get_comments(1)
        self.assertNotEquals(False, response)

    def test_get_aspect_ratio(self):
        folder = Folder()
        response = folder.upload_file('./data/test_convert_slide.pptx')
        self.assertEqual(True, response)

        doc = Extractor('test_convert_slide.pptx')
        response = doc.get_aspect_ratio(1)
        self.assertNotEquals(False, response)

    def test_convert_additonal_params(self):
        folder = Folder()
        response = folder.upload_file('./data/test_convert_slide.pptx')
        self.assertEqual(True, response)

        converter = Converter('test_convert_slide.pptx')
        converter.convert('tiff')

    def test_convert_storage_file(self):
        folder = Folder()
        response = folder.upload_file('./data/test_convert_slide.pptx')
        self.assertEqual(True, response)

        converter = Converter('test_convert_slide.pptx')
        converter.convert('tiff')
        self.assertTrue(os.path.exists('./output/test_convert_slide.tiff'))

    def test_get_shape(self):
        folder = Folder()
        response = folder.upload_file('./data/test_convert_slide.pptx')
        self.assertEqual(True, response)

        ex = Extractor('test_convert_slide.pptx')
        response = ex.get_shape(1,1)
        self.assertNotEquals(False, response)


if __name__ == '__main__':
    unittest.main()
