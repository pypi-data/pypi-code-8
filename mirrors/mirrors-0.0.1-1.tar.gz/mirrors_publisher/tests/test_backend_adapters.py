import logging
import shutil
from unittest import mock

from django.conf import settings
from django.test import TestCase

from mirrors_publisher import backend_adapters


class MockAdapter(object):
    def __init__(self, *args, **kwargs):
        pass

    def put(self, dest, file):
        pass


class BackendAdapterTest(TestCase):
    def setUp(self):
        self.orig_adapter = settings.BACKEND_ADAPTER
        self.orig_adapter_args = settings.BACKEND_ADAPTER_ARGS

        settings.BACKEND_ADAPTER = 'mirrors_publisher.tests.'
        settings.BACKEND_ADAPTER += 'test_backend_adapters.MockAdapter'
        settings.BACKEND_ADAPTER_ARGS = {
            'fs_root': 'the root'
        }

    def tearDown(self):
        settings.BACKEND_ADAPTER = self.orig_adapter
        settings.BACKEND_ADAPTER_ARGS = self.orig_adapter_args

    def test_base_put_fail(self):
        ba = backend_adapters.BackendAdapter()
        with self.assertRaises(NotImplementedError):
            ba.put(None, None)

    def test_get_adapter(self):
        # not currently sure how to properly mock this because patching getattr
        # seems to cause a boatload of problems
        adapter = backend_adapters.get_adapter()
        self.assertIsInstance(adapter, MockAdapter)


class LocalFSAdapterTest(TestCase):
    def setUp(self):
        self.adapter = backend_adapters.LocalFSAdapter(fs_root='/fs_root')
        logging.disable(logging.CRITICAL)

    def tearDown(self):
        logging.disable(logging.NOTSET)

    def test_undefined_fs_root(self):
        self.adapter.kwargs = {}

        with self.assertRaises(AssertionError):
            self.adapter.put(None, None)

    @mock.patch('mirrors_publisher.backend_adapters.tempfile.'
                'NamedTemporaryFile')
    @mock.patch('os.path')
    @mock.patch('os.makedirs')
    @mock.patch('shutil.copyfile')
    def test_missing_fs_root_and_dest_dir(self,
                                          p_copyfile,
                                          p_makedirs,
                                          p_path,
                                          p_tempfile):
        p_path.isdir.return_value = False
        p_path.join.return_value = 'real_dest_value'
        p_path.abspath.return_value = 'abspath_value'
        p_path.dirname.return_value = 'dest_dir_value'

        ntf = mock.Mock()
        ntf.configure_mock(name='tempfilename')
        p_tempfile.return_value = ntf

        result = self.adapter.put('dest', bytes('file data', 'UTF-8'))

        p_path.isdir.assert_has_calls([mock.call('/fs_root'),
                                       mock.call('dest_dir_value')])

        p_path.dirname.assert_call('real_dest_value')
        p_makedirs.assert_has_calls([mock.call('/fs_root', 0o774),
                                     mock.call('dest_dir_value', 0o774)])

        p_path.join.assert_called_once_with('/fs_root', 'dest')

        p_path.abspath.assert_called_once_with('tempfilename')
        p_copyfile.assert_called_once_with('abspath_value', 'real_dest_value')
        ntf.close.assert_called_once_with()

        self.assertEquals(result, 'real_dest_value')

    @mock.patch('mirrors_publisher.backend_adapters.logging')
    @mock.patch('mirrors_publisher.backend_adapters.tempfile.'
                'NamedTemporaryFile')
    @mock.patch('os.path')
    @mock.patch('mirrors_publisher.backend_adapters.shutil')
    def test_shutil_call_fails(self, p_shutil, p_path, p_tempfile, p_logging):
        p_path.isdir.return_value = True
        p_path.join.return_value = 'real_dest_value'
        p_path.abspath.return_value = 'abspath_value'
        p_path.dirname.return_value = 'dest_dir_value'

        ntf = mock.Mock()
        ntf.configure_mock(name='tempfilename')
        p_tempfile.return_value = ntf

        p_shutil.copyfile = mock.Mock(spec=shutil.copyfile,
                                      side_effect=OSError)

        result = self.adapter.put('dest', bytes('file data', 'UTF-8'))

        p_shutil.copyfile.assert_called_once_with('abspath_value',
                                                  'real_dest_value')
        p_logging.exception.assert_called_once()

        self.assertIsNone(result)
