# -*- coding: utf-8 -*-
"""
uh.cx API interface

http://uh.cx/
"""

import unittest

import uhcx


class Tests(unittest.TestCase):
    def testCreateLink(self):
        url = 'http://www.google.de/'
        link = uhcx.Manager.create(url)

        self.assertIsNotNone(link)
        self.assertEqual(url, link.url_original)

    def testCreateInvalidLink(self):
        self.assertRaises(uhcx.Manager.CouldNotCreateLinkException, uhcx.Manager.create, 'asd')


def main():
    unittest.main()


if __name__ == '__main__':
    main()
