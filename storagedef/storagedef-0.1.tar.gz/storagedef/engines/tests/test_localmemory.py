# -*- coding: utf-8 -*-

import unittest


class MemoryStorageEngineTestCase(unittest.TestCase):

    def test_delete(self):
        from ..localmemory import LocalMemoryStorageEngine
        engine = LocalMemoryStorageEngine()
        engine.storage['test.ext'] = b'test content'
        engine.delete('test.ext')
        self.assertDictEqual(engine.storage, {})

    def test_exists_false(self):
        from ..localmemory import LocalMemoryStorageEngine
        engine = LocalMemoryStorageEngine()
        self.assertFalse(engine.exists(b'test.ext'))

    def test_exists_true(self):
        from ..localmemory import LocalMemoryStorageEngine
        engine = LocalMemoryStorageEngine()
        engine.storage['test.ext'] = b'test content'
        self.assertTrue(engine.exists('test.ext'))

    def test_retrieve_not_found(self):
        from ...exceptions import DoesNotExist
        from ..localmemory import LocalMemoryStorageEngine
        engine = LocalMemoryStorageEngine()
        self.assertRaises(DoesNotExist, engine.retrieve, 'test.ext')

    def test_retrieve_found(self):
        from ..localmemory import LocalMemoryStorageEngine
        engine = LocalMemoryStorageEngine()
        engine.storage['test.ext'] = b'test content'
        fobj = engine.retrieve('test.ext')
        self.assertTrue(hasattr(fobj, 'read'))
        self.assertEqual(fobj.read(), b'test content')

    def test_store(self):
        from io import BytesIO
        from ..localmemory import LocalMemoryStorageEngine
        engine = LocalMemoryStorageEngine()
        engine.store('test.ext', BytesIO(b'test content'))
        self.assertDictEqual(engine.storage, {'test.ext': b'test content'})
