# -*- coding: utf-8 -*- 
from main import EpubWorker
import unittest
# import subprocess

class TestMainPy(unittest.TestCase):
    def setUp(self):
        pass


WRONG_REQUEST = {'results': []}
RIGHT_REQUEST = {'baseCfi': '/6/24[id15]!', 'title': '', 'path': './tmp/Sensei4//index_split_011.html',
                              'href': 'index_split_011.html', 'cfi': '/6/24[id15]!/4/62'}
CHARACTER_CFI = ['/6/2[id116]', '/6/4[id115]', '/6/6[id114]', '/6/8[id113]', '/6/10[id112]', '/6/12[id111]', '/6/14[id110]',
 '/6/16[id19]', '/6/18[id18]', '/6/20[id17]', '/6/22[id16]', '/6/24[id15]', '/6/26[id14]', '/6/28[id13]', '/6/30[id12]', '/6/32[id11]']


class TestEpubWorker(unittest.TestCase):
    def setUp(self):
        test_dir = './test_data/'
        self.epub_dir = EpubWorker(test_dir + 'Sensei4/')
        self.epub_file = EpubWorker(test_dir + 'Sensei4.epub')

    def test_search_in_dir(self):
        self.assertDictEqual(self.epub_dir.search_word('хряк'), WRONG_REQUEST)
        self.assertDictEqual(self.epub_dir.search_word('аллат')['results'][0], RIGHT_REQUEST)

    def test_search_in_epub(self):
        self.assertDictEqual(self.epub_file.search_word('хряк'), WRONG_REQUEST)
        self.assertDictEqual(self.epub_file.search_word('аллат')['results'][0], RIGHT_REQUEST)

    def test_force_index(self):
        pass

    def test_get_old_book_from_index(self):
        pass

    def test_get_character_cfi(self):
        self.assertEqual(self.epub_file.get_characters_cfi(), CHARACTER_CFI)
        self.assertEqual(self.epub_dir.get_characters_cfi(), CHARACTER_CFI)


if __name__ == '__main__':
    unittest.main()

