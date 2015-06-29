__author__ = 'Stephan Conrad <stephan@conrad.pics>'

from exon.utils.fileutils import readfile, readfileAsArray,writefile,writefileFromArray
import unittest
import tempfile
import os


class FileUtilTest(unittest.TestCase):

    def setUp(self):
        self.tempdir = tempfile.gettempdir()
        self.file = os.path.join(self.tempdir, 'exon-unit-test-file.txt')
        self.data = [
            'Unit',
            'Test'
        ]

    def tearDown(self):
        if os.path.exists(self.file):
            os.remove(self.file)

    def test_WrtieFile(self):
        writefile(self.file, '\n'.join(self.data))
        self.assertTrue(os.path.isfile(self.file))
        content = readfile(self.file)
        self.assertEqual('\n'.join(self.data), content)

    def test_WritFileFromArray(self):
        writefileFromArray(self.file, self.data)
        self.assertTrue(os.path.isfile(self.file))
        self.assertEqual(self.data, readfileAsArray(self.file))