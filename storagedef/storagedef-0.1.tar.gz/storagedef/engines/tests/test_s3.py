# -*- coding: utf-8 -*-

import os
import unittest


class S3StorageEngineTestCase(unittest.TestCase):

    @unittest.skipUnless('X_TESTING_S3BUCKET' in os.environ,
                         'require environment variable X_TESTING_S3BUCKET')
    def test(self):
        import io
        from ..s3 import S3StorageEngine
        from ...exceptions import DoesNotExist
        engine = S3StorageEngine(bucket=os.environ['X_TESTING_S3BUCKET'])
        engine.delete('testing.txt')
        self.assertFalse(engine.exists('testing.txt'))
        self.assertRaises(DoesNotExist, engine.retrieve, 'testing.txt')
        engine.store('testing.txt', io.BytesIO(b'testcontent'))
        self.assertTrue(engine.exists('testing.txt'))
        ret = engine.retrieve('testing.txt')
        self.assertEqual(ret.read(), b'testcontent')
