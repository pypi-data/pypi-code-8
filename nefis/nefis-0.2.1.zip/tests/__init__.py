from unittest import TestCase

import nefis_attributes
import nefis_define
import nefis_doc_strings
import nefis_getels_strings
import nefis_getelt_floats
import nefis_getelt_integers
import nefis_get_headers
import nefis_inquire
import nefis_putels_strings
import nefis_putelt_floats
import nefis_putelt_integers

class Testen(TestCase):
    def test01(self):
        nefis_attributes.test_nefis_attributes()
    def test02(self):
        nefis_define.test_nefis_define()
    def test03(self):
        nefis_doc_strings.print_doc()
    def test04(self):
        nefis_putels_strings.test_nefis_putels_strings()
    def test05(self):
        nefis_getelt_floats.test_nefis_getelt_floats()
    def test06(self):
        nefis_getelt_integers.test_nefis_getelt_integers()
    def test07(self):
        nefis_get_headers.test_nefis_get_headers()
    def test08(self):
        nefis_inquire.test_nefis_inquire()
    def test09(self):
        nefis_getels_strings.test_nefis_getels_strings()
    def test10(self):
        nefis_putelt_floats.test_nefis_putelt_floats()
    def test11(self):
        nefis_putelt_integers.test_nefis_putelt_integers()    
