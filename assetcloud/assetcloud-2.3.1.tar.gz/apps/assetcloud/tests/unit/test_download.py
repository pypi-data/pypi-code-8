# (c) 2011 Bright Interactive Limited. All rights reserved.
# http://www.bright-interactive.com | info@bright-interactive.com

"""
Unit Tests for downloads.

Tests in this module are unit tests, and therefore:
 - must run quickly,
 - must have minimal dependencies (for example, they must not use a database).
"""

import assetcloud.download
import tempfile
import os

from .utils import UnitTestCase


class MockAsset(object):
    def __init__(self):
        self.filename = None

    @property
    def basename(self):
        return self.filename


class DownloadHeaderTests(UnitTestCase):
    """
    Tests for response headers that are sent for asset downloads.
    """

    def test_content_disposition_and_type(self):
        mock_asset = MockAsset()
        mock_asset.filename = 'foo.jpg'
        mock_request = dict()
        assetcloud.download.set_download_headers_for_asset(mock_request, mock_asset)

        # set_download_headers_for_asset should have added 2 and only 2
        # headers (Content-Disposition and Content-Type)
        self.assertEqual(2, len(mock_request))

        self.assertEqual('attachment; filename="foo.jpg"',
                         mock_request['Content-Disposition'])
        self.assertEqual('image/jpeg',
                         mock_request['Content-Type'])

    def test_content_disposition_filename_contains_space(self):
        mock_asset = MockAsset()
        mock_asset.filename = 'foo bar.jpg'
        mock_request = dict()
        assetcloud.download.set_download_headers_for_asset(mock_request, mock_asset)

        self.assertEqual('attachment; filename="foo bar.jpg"',
                         mock_request['Content-Disposition'])

    def test_content_disposition_filename_contains_quote(self):
        mock_asset = MockAsset()
        mock_asset.filename = 'foo "bar.jpg'
        mock_request = dict()
        assetcloud.download.set_download_headers_for_asset(mock_request, mock_asset)

        self.assertEqual('attachment; filename="foo \\"bar.jpg"',
                         mock_request['Content-Disposition'])


class DeleteAfterwardsFileResponseTests(UnitTestCase):
    def test_delete_response_deletes_on_close(self):
        named_file = tempfile.NamedTemporaryFile(delete=False)
        try:
            named_file.write('test')
            self.assertTrue(os.path.exists(named_file.name))
            delete_response = assetcloud.download.DeleteAfterwardsFileResponse(
                path=named_file.name)
            delete_response.close()
            self.assertFalse(os.path.exists(named_file.name))
        finally:
            try:
                os.remove(named_file.name)
            except (OSError, IOError):
                pass
