# coding: utf-8
""" Tests for pypel.cli.

THIS SOFTWARE IS UNDER BSD LICENSE.
Copyright (c) 2012-2015 Daniele Tricoli <eriol@mornie.org>

Read LICENSE for more informations.
"""

import unittest

from pypel.cli import Row, Table


class RowTestCase(unittest.TestCase):

    def test_empty(self):
        row = Row()

        self.assertEqual(row.len(), None)
        with self.assertRaises(TypeError):
            row.format()
        with self.assertRaises(KeyError):
            row.format('price')

    def test_float(self):
        row = Row({'price': 2.71})

        self.assertEqual(row.len('price'), 4)
        self.assertEqual(row.format('price'), '{price:>{price_len}.2f}')

    def test_int(self):
        row = Row({'price': 2})

        self.assertEqual(row.len('price'), 1)
        self.assertEqual(row.format('price'), '{price:{price_len}}')

    def test_str(self):
        row = Row({'note': 'A simply note.'})
        self.assertEqual(row.len('note'), 14)
        self.assertEqual(row.format('note'), '{note:{note_len}}')


class TableTestCase(unittest.TestCase):

    def setUp(self):
        self.table = Table()

    def test_empty(self):
        self.assertEqual(self.table.rows, [])
        self.assertEqual(self.table.max_len, {})

    def test_add_new_row(self):
        row = Row({'file': 'receipt.jpg',
                   'price': 2.71,
                   'retailer': 'カオナシ',
                   'note': 'An useless note.'})
        self.table.add_row(row)

        self.assertEqual(len(self.table.rows), 1)
        self.assertEqual(''.join(self.table.to_string()),
                         'receipt.jpg -- 2.71 -- カオナシ -- An useless note.')


class TableToStringTestCase(unittest.TestCase):

    def setUp(self):
        self.table = Table()
        row = Row({'file': 'receipt.jpg',
                   'price': 2.71,
                   'retailer': 'カオナシ',
                   'note': 'An useless note.'})
        self.table.add_row(row)

    def test_fields_order(self):
        order = ['price', 'note', 'file', 'retailer']
        self.assertEqual(''.join(self.table.to_string(fields_order=order)),
                         '2.71 -- An useless note. -- receipt.jpg -- カオナシ')

    def test_separator(self):
        sep = ' * '
        self.assertEqual(''.join(self.table.to_string(sep=sep)),
                         'receipt.jpg * 2.71 * カオナシ * An useless note.')

    def test_verify(self):
        self.table.rows[0].update(dict(verified=False))
        self.assertEqual(''.join(self.table.to_string(verify=True)),
                         'receipt.jpg -- 2.71 -- カオナシ -- An useless note.'
                         ' | False')
        self.table.rows[0].update(dict(verified=True))
        self.assertEqual(''.join(self.table.to_string(verify=True)),
                         'receipt.jpg -- 2.71 -- カオナシ -- An useless note.'
                         ' | True')
