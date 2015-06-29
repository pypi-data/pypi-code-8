__author__ = 'Stephan Conrad <stephan@conrad.pics>'

import unittest
from exon.http import ExonHttpsClient

class ExonHttpsTestCase(unittest.TestCase):
    def setUp(self):
        self.conn = ExonHttpsClient(
            host='localhost',
            port=3000,
            cafile='/etc/exon/ca/certs/exon.ca.cert.pem',
            user='admin',
            password='admin123',
            check_hostname=False
        )

    def tearDown(self):
        self.conn.close()

    def assertHttpOk(self, status, msg=None):
        super().assertEqual(status, 200, msg)


