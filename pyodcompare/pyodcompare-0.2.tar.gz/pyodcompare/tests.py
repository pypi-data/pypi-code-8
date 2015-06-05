import os
import subprocess
import datetime
from unittest import TestCase
from pyodcompare import DocumentCompare, DocumentCompareException

TEST_DATA_PATH = os.path.normpath(os.path.join(os.path.dirname(__file__),
                                               'test_data'))
V1_PATH = os.path.join(TEST_DATA_PATH, 'documentv1.doc')
V2_PATH = os.path.join(TEST_DATA_PATH, 'documentv2.doc')
COMPARE_PATH = os.path.join(TEST_DATA_PATH, 'documentdiff.odt')


class DocumentCompareTest(TestCase):

    def setUp(self):
        self.compare = DocumentCompare(listener=('localhost', 2002))

    def test_fail_connect(self):
        with self.assertRaises(DocumentCompareException):
            DocumentCompare(listener=('localhost', 1337))

    def test_not_existing_document(self):
        with self.assertRaises(DocumentCompareException):
            self.compare.compare("kittens.docx", "docs.pdf", COMPARE_PATH)

        with self.assertRaises(DocumentCompareException):
            self.compare.compare(V1_PATH, "kittens.docx", COMPARE_PATH)

    def test_fill_data(self):
        self.compare.compare(V1_PATH, V2_PATH, COMPARE_PATH)
        self.assertTrue(os.path.exists(COMPARE_PATH))

    def tearDown(self):
        """
        Cleanup
        """
        if os.path.exists(COMPARE_PATH):
            os.remove(COMPARE_PATH)
