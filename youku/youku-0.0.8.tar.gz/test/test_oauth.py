# -*- coding: utf-8 -*-
import os
import sys
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import unittest
from config import *
from youku import YoukuOauth


class OauthTest(unittest.TestCase):
    def setUp(self):
        self.youku = YoukuOauth(CLIENT_ID, CLIENT_SECRET, REDIRECT_URI)

    def test_refresh_token(self):
        result = self.youku.refresh_token(REFRESH_TOKEN)
        print_json(result)

if __name__ == '__main__':
    unittest.main()
