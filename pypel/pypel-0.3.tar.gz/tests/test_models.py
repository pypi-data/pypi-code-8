# coding: utf-8
""" Tests for pypel.models.

THIS SOFTWARE IS UNDER BSD LICENSE.
Copyright (c) 2012-2015 Daniele Tricoli <eriol@mornie.org>

Read LICENSE for more informations.
"""

import tempfile
import unittest

from PIL import Image

from pypel.models import Receipt, set_metadata, delete_metadata, make_receipt
from pypel.models import DoesNotExist, IsADirectory, ImageNotSupported


class ReceiptSetUpTestCase(unittest.TestCase):
    """Create a temporary receipt."""

    def setUp(self):

        self.tmp_file = tempfile.NamedTemporaryFile()

        self.size = 100, 100
        self.image = Image.new('RGB', self.size)
        self.image.save(self.tmp_file.name, format='PNG')

        self.receipt = Receipt(self.tmp_file.name)

    def tearDown(self):
        self.tmp_file.close()


class ReceiptMetadataTestCase(ReceiptSetUpTestCase):

    def test_price(self):
        """Set/get price for receipt."""
        self.receipt.price = 8.27
        self.assertEqual(self.receipt.price, 8.27)

        del self.receipt.price
        self.assertEqual(self.receipt.price, None)

    def test_retailer(self):
        """Set/get retailer for receipt."""
        self.receipt.retailer = 'Bazaar'
        self.assertEqual(self.receipt.retailer, 'Bazaar')

        del self.receipt.retailer
        self.assertEqual(self.receipt.retailer, None)

    def test_note(self):
        """Set/get note for receipt."""
        self.receipt.note = 'A book worth reading is worth buying.'
        self.assertEqual(self.receipt.note,
                         'A book worth reading is worth buying.')

        del self.receipt.note
        self.assertEqual(self.receipt.note, None)

    def test_set_metadata(self):
        """Test set_metadata command."""

        self.assertEqual(self.receipt.price, None)
        self.assertEqual(self.receipt.retailer, None)
        self.assertEqual(self.receipt.note, None)

        set_metadata(self.receipt, price=8.27)
        self.assertEqual(self.receipt.price, 8.27)
        self.assertEqual(self.receipt.retailer, None)
        self.assertEqual(self.receipt.note, None)

        set_metadata(self.receipt, retailer='Bazaar')
        self.assertEqual(self.receipt.retailer, 'Bazaar')
        self.assertEqual(self.receipt.note, None)

        set_metadata(self.receipt, note='This is a note.')
        self.assertEqual(self.receipt.note, 'This is a note.')

    def test_delete_metadata(self):
        """Test delete_metadata command."""

        set_metadata(self.receipt,
                     price=8.27,
                     retailer='Bazaar',
                     note='A note')

        self.assertEqual(self.receipt.price, 8.27)
        self.assertEqual(self.receipt.retailer, 'Bazaar')
        self.assertEqual(self.receipt.note, 'A note')

        delete_metadata(self.receipt, price=True)
        self.assertEqual(self.receipt.price, None)

        delete_metadata(self.receipt, retailer=True)
        self.assertEqual(self.receipt.retailer, None)

        delete_metadata(self.receipt, note=True)
        self.assertEqual(self.receipt.note, None)

        set_metadata(self.receipt,
                     price=8.27,
                     retailer='Bazaar',
                     note='A note')
        delete_metadata(self.receipt)

        self.assertEqual(self.receipt.price, None)
        self.assertEqual(self.receipt.retailer, None)
        self.assertEqual(self.receipt.note, None)

    def test_asdict(self):
        set_metadata(self.receipt,
                     price=8.27,
                     retailer='Bazaar',
                     note='A note')
        self.assertEqual(self.receipt.asdict(),
                         {'file': self.tmp_file.name,
                          'price': 8.27,
                          'retailer': 'Bazaar',
                          'note': 'A note'})


class MakeReceiptTestCase(unittest.TestCase):

    def setUp(self):
        self.tmp_file_png = tempfile.NamedTemporaryFile(suffix='.png')
        self.tmp_file_txt = tempfile.NamedTemporaryFile(suffix='.txt')

        self.size = 10, 10
        self.image = Image.new('RGB', self.size)
        self.image.save(self.tmp_file_png.name, format='PNG')

        self.receipt = Receipt(self.tmp_file_png.name)

    def tearDown(self):
        self.tmp_file_png.close()
        self.tmp_file_txt.close()

    def test_does_not_exist(self):
        """Raise DoesNotExist if specified file does not exists."""
        self.assertRaises(DoesNotExist,
                          make_receipt,
                          '/it/is/very/difficult/that/this/path/exists/really/')

    def test_is_a_directory(self):
        """Raise IsADirectory if a directory is specified."""
        self.assertRaises(IsADirectory, make_receipt, '/')

    def test_image_not_supported(self):
        """Raise ImageNotSupported if specified image file is not supported."""
        self.assertRaises(ImageNotSupported,
                          make_receipt,
                          self.tmp_file_txt.name)

    def test_receipt_creation(self):
        """Create a Receipt using make_receipt factory function."""
        r = make_receipt(self.tmp_file_png.name)
        self.assertTrue(isinstance(r, Receipt))
