# -*- coding: utf-8 -*-

import unittest


class SessionTestCase(unittest.TestCase):

    def test_load_localmemory(self):
        from ..session import Session
        from ..engines.localmemory import LocalMemoryStorageEngine
        session = Session.from_config({
            'provider':
                'storagedef.engines.localmemory:LocalMemoryStorageEngine',
        })
        self.assertIsInstance(session.engine, LocalMemoryStorageEngine)

    def test_load_s3(self):
        from ..session import Session
        from ..engines.s3 import S3StorageEngine
        session = Session.from_config({
            'provider': 'storagedef.engines.s3:S3StorageEngine',
            'bucket': 'mybucket',
        })
        self.assertIsInstance(session.engine, S3StorageEngine)
