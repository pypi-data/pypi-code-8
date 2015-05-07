# (c) 2011 Bright Interactive Limited. All rights reserved.
# http://www.bright-interactive.com | info@bright-interactive.com
from assetcloud.random_utils import random_image_file
from assetcloud.tests.service.utils import TestCase, LoggedInTestCase, \
    RoleTest, create_asset, create_image_asset
from django.core.urlresolvers import reverse
from email.utils import quote
import PIL
import StringIO
import decimal


def _resize_asset_test_setup(self):
    self.format = 'png'
    self.asset = create_image_asset(suffix='.%s' % self.format,
                                    account=self.account)


class ResizeAssetsRoleTests(LoggedInTestCase):
    """
    Check that asset resizing works and that the correct roles have access to
    it.
    """

    class RoleTestResize(RoleTest):
        can = ['viewer', 'editor', 'admin']

        def given(self, test):
            _resize_asset_test_setup(test)

        def when(self, test):
            self.width = 50
            self.height = 50
            return test.client.get(reverse('asset-resize-download-action',
                                           kwargs={'id': test.asset.id,
                                                   'width': self.width,
                                                   'height': self.height}))

        def role_can(self, test, response):
            test.assertEquals(response.status_code, 200)
            infile = StringIO.StringIO(response.content)

            image = PIL.Image.open(infile)
            infile.close()
            test.assertEqual(image.size, (self.width, self.height))


class ResizeAssetsTests(LoggedInTestCase):
    """
    Check that asset resizing works
    """

    def setUp(self):
        super(ResizeAssetsTests, self).setUp()
        _resize_asset_test_setup(self)

    def test_resize_maintains_aspect_ratio(self):
        width = 50
        response = self.client.get(reverse('asset-resize-download-width-action',
                                           kwargs={'id': self.asset.id,
                                                   'width': width}))
        self.assertEquals(response.status_code, 200)
        infile = StringIO.StringIO(response.content)

        image = PIL.Image.open(infile)
        infile.close()

        self.asset.file.seek(0)
        original_image = PIL.Image.open(self.asset.file)
        original_width, original_height = original_image.size
        expected_height = (decimal.Decimal(original_height) / decimal.Decimal(original_width) * decimal.Decimal(width)).quantize(1)

        self.assertEqual(image.size, (width, expected_height))

    def test_resize_is_95_quality(self):
        self.asset = create_image_asset(suffix='.jpeg', account=self.account)
        response = self.client.get(reverse('asset-resize-download-width-action',
                                           kwargs={'id': self.asset.id,
                                                   'width': 50}))
        resized_image = StringIO.StringIO(response.content)
        self.asset.file.seek(0)

        original_image = PIL.Image.open(self.asset.file)
        width = decimal.Decimal(50)
        iwidth, iheight = original_image.size
        height = decimal.Decimal(iheight) / decimal.Decimal(iwidth) * width

        correct_quality_image = StringIO.StringIO()
        original_image.resize((width.quantize(1), height.quantize(1))).save(
            correct_quality_image, 'jpeg', quality=90)
        try:
            self.assertEqual(correct_quality_image.getvalue(),
                             resized_image.read())
        finally:
            resized_image.close()
            correct_quality_image.close()


class ResizeAssetsFilenameTests(LoggedInTestCase):
    def test_resize_link_shown_for_image_asset(self):
        asset = create_image_asset(suffix='.png',
                                   account=self.account)
        self.assertContainsResizeLink(asset)

    def test_resize_link_not_shown_for_no_mimetype_filename(self):
        """
        Make sure that the "download resized" links aren't shown on the asset
        page when the asset filename is '.png', because
        mimetypes.guess_type('.png') returns (None, None) for '.png', and
        also os.path.splitext('.png') thinks that '.png' is a basename not an
        extension.
        """
        # We have to create the asset first and then change its filename because
        # random_image_file(), which is used by create_image_asset(), treats
        # '.png' as a basename of '.png' with no extension, so it can't work
        # out what format arg to pass to PIL.Image.save()
        asset = create_asset(filename='.png',
                             file_obj=random_image_file(),
                             account=self.account)
        asset.save()
        self.assertNotContainsResizeLink(asset)

    def assertContainsResizeLink(self, asset):
        response = self.get_asset_page(asset)
        self.assertContains(response, 'Custom size...')

    def assertNotContainsResizeLink(self, asset):
        response = self.get_asset_page(asset)
        self.assertNotContains(response, 'Custom size...')

    def get_asset_page(self, asset):
        url = reverse('asset', kwargs={'id': asset.id})
        response = self.client.get(url)
        # Ensure all the page is rendered with the correct template,
        # and the correct asset.
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'assetcloud/pages/asset.html')
        self.assertEquals(asset, response.context['asset'])
        return response


class DownloadAssetsRoleTests(TestCase):

    class RoleTestDownload(RoleTest):
        """
        Test that file downloads okay, and its content is correct.
        """
        can = ['viewer', 'admin', 'editor']

        def given(self, test):
            self.asset = create_asset(account=test.account)

        def when(self, test):
            return test.client.get(reverse('asset-download-action',
                                           kwargs={'id': self.asset.id}))

        def role_can(self, test, response):
            test.assertEquals(response.status_code, 200)
            test.assertEquals(response.content, self.asset.file.read())


class DownloadAssetsTests(LoggedInTestCase):
    """
    Check that we can download assets, and that the various HTTP headers are
    set correctly.
    Note that this really only applies to development servers.
    In production assets should be served directly by the web server.
    """

    def setUp(self):
        super(DownloadAssetsTests, self).setUp()
        self.asset = create_asset(account=self.account)

    def test_download_filename(self):
        """
        Test that file downloads okay, and its filename is correct.
        """
        response = self.client.get(reverse('asset-download-action',
                                           kwargs={'id': self.asset.id}))
        self.assertEquals(response.status_code, 200)
        self.assertEquals(response['Content-Disposition'],
                          'attachment; filename="%s"' %
                          quote(self.asset.basename))

    def test_download_where_file_is_image(self):
        """
        Test that the relevant mime-type is included in the response.
        """
        self.assert_download_mimetype_is_image_png('picture.png')

    def test_download_mimetype_with_dollar_and_extension_filename(self):
        self.assert_download_mimetype_is_image_png('$.png')

    def test_download_content_encoding_with_dollar_and_extension_filename(self):
        # This tests the Content-Type and Content-Encoding code in
        # AssetDownloadHeaderGenerator.set_download_headers_for_asset. The
        # filename '$.tgz' is carefully chosen such that '$.tgz' will be
        # assinged an encoding by mimetypes.guess_type but '.tgz'
        # won't. Don't change it to '$.tar.gz' because '.tar.gz' *is*
        # assigned an encoding by mimetypes.guess_type so that change would
        # make this test succeed even without the Content-Encoding code in
        # set_download_headers_for_asset.
        self.asset = create_asset(filename='$.tgz', account=self.account)
        response = self.client.get(reverse('asset-download-action',
                                           kwargs={'id': self.asset.id}))
        self.assertEquals(response.status_code, 200)
        self.assertEquals(response['Content-Type'], 'application/x-tar')
        self.assertEquals(response['Content-Encoding'], 'gzip')

    def test_download_mimetype_with_nasty_filename(self):
        self.assert_download_mimetype_is_image_png('hxP\<kG.png')

    def assert_download_mimetype_is_image_png(self, filename):
        self.asset = create_image_asset(filename=filename, account=self.account)
        response = self.client.get(reverse('asset-download-action',
                                           kwargs={'id': self.asset.id}))
        self.assertEquals(response.status_code, 200)
        self.assertEquals(response['Content-Type'], 'image/png')
