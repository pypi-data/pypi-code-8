# (c) 2011 Bright Interactive Limited. All rights reserved.
# http://www.bright-interactive.com | info@bright-interactive.com
from assetcloud import upload_history, random_utils
from assetcloud.models import Asset, Upload
from assetcloud.random_utils import random_image_file
from assetcloud.tests.service.utils import LoggedInTestCase, RoleTest, create_fake_request, create_user, create_asset
from contextlib import contextmanager
from django.core.urlresolvers import reverse
from django.test.utils import override_settings
from sorl.thumbnail import default
import StringIO
import json


def setup_example_files(self):
    self.file_name = 'example.txt'
    self.file_contents = 'examplecontents'
    # In-memory file object.
    self.file = StringIO.StringIO(self.file_contents)
    self.file.name = self.file_name
    # Second in-memory file object.
    self.file2 = StringIO.StringIO(self.file_contents)
    self.file2.name = self.file_name


class UploadTests(LoggedInTestCase):
    """
    Test Asset Upload.
    """

    def setUp(self):
        super(UploadTests, self).setUp()
        setup_example_files(self)

    class RoleTestUpload(RoleTest):
        can = ['admin', 'editor']
        cant = ['viewer']

        def when(self, test):
            # Upload the file.
            return test.client.post(reverse('asset-upload-action'),
                                    {'file': test.file})

        def role_can(self, test, response):
            test.assertRedirects(response, reverse('asset-upload'))

            # Check the Asset instance.
            asset = Asset.objects(test.user).order_by('-id')[0]

            test.assertEqual(asset.basename, test.file_name)
            test.assertEqual(asset.title, Asset.infer_title(test.file_name))
            test.assertEqual(asset.file.read(), test.file_contents)
            test.assertEqual(asset.added_by, test.client.logged_in_user)

            test.assertEqual({asset}, set(upload_history.last_upload_assets(test.user)))

    def test_multiple_upload(self):
        """
        Test that asset upload also accepts multiple files.
        """
        # Upload the files.
        # For test simplicity we'll just use two identical files.
        initial_number_of_assets = Asset.objects(self.user).count()

        response = self.client.post(reverse('asset-upload-action'),
                                    {'file': [self.file, self.file2]})
        self.assertRedirects(response, reverse('asset-upload'))

        # Check the Asset instances.
        self.assertEquals(Asset.objects(self.user).count(),
                          initial_number_of_assets + 2)

        assets = Asset.objects(self.user).order_by("-id")[:2]
        for asset in assets:
            self.assertEquals(asset.basename, self.file_name)
            self.assertEquals(asset.file.read(), self.file_contents)

        self.assertEqual(set(assets),
                         set(upload_history.last_upload_assets(self.user)))

    def test_repeated_filename_upload(self):
        """
        Test that you can upload more than one asset with the
        same filename, and that both assets will have the same
        filename attached.
        """

        # Upload the files.
        response = self.client.post(reverse('asset-upload-action'),
                                    {'file': self.file})
        self.assertRedirects(response, reverse('asset-upload'))

        response = self.client.post(reverse('asset-upload-action'),
                                    {'file': self.file})
        self.assertRedirects(response, reverse('asset-upload'))

        # Check the Asset instances.
        assets = Asset.objects(self.user).order_by('-id')
        asset_1 = assets[0]
        asset_2 = assets[1]
        self.assertEquals(asset_1.basename, self.file_name)
        self.assertEquals(asset_2.basename, self.file_name)

    @contextmanager
    def assertFunctionIsCalled(self, fn):
        called = {}

        def new_fn(*args, **kwargs):
            called['args'] = args
            called['kwargs'] = kwargs
            return fn(*args, **kwargs)

        cls = fn.__self__
        original_attr = None
        for attr in dir(cls):
            if getattr(cls, attr) == fn:
                original_attr = attr
                setattr(cls, attr, new_fn)
                break
        yield

        self.assertTrue(called, 'Function %s was not called (%s)' % (original_attr, fn))
        setattr(cls, original_attr, fn)

    def test_upload_automatically_creates_thumbnail(self):
        with self.assertFunctionIsCalled(default.backend._create_thumbnail):
            image_file = random_utils.random_image_file()
            self.client.post(reverse('asset-upload-action'),
                             {'file': image_file})

    def test_cancel_action_posts_message(self):
        create_fake_request(self.user)
        self.assertResponseContains(
            'Your upload has been cancelled',
            self.client.get(reverse('cancel_upload_action'), follow=True))

    def test_upload_sets_image_info(self):
        f = random_image_file()
        self.client.post(reverse('asset-upload-action'),
                         {'file': f})

        # Check the Asset instance.
        asset = Asset.unrestricted_objects.get()
        self.assertTrue(asset.image_info)

    def test_upload_long_filename(self):
        f = random_image_file(filename='furniture_chairs_hirshorn_vintage_union_jack_denim_chair.png',
                              suffix='.png')
        response = self.client.post(
            reverse('asset-upload-action'),
            {'file': f},
            follow=True)
        self.assertEqual(200, response.status_code)

        # Check the Asset instance.
        asset = Asset.unrestricted_objects.get()
        self.assertEqual(asset.filename, 'furniture_chairs_hirshorn_vintage_union_jack_denim_chair.png')


class AjaxUploadTests(LoggedInTestCase):

    def setUp(self):
        super(AjaxUploadTests, self).setUp()
        setup_example_files(self)

    class RoleTestAjaxUpload(RoleTest):
        can = ['admin', 'editor']
        cant = ['viewer']

        def when(self, test):
            # Upload the file, with a header indicating it's an AJAX request
            return test.client.post(reverse('asset-upload-action'),
                                    {'file': test.file},
                                    HTTP_X_REQUESTED_WITH='XMLHttpRequest')

        def role_can(self, test, response):
            test.assertEqual(200, response.status_code)

            jsonrpc_response = json.loads(response.content)
            test.assertIn('result', jsonrpc_response)
            test.assertNotIn('error', jsonrpc_response)

            # Check the Asset instance.
            asset = Asset.objects(test.user).order_by('-id')[0]

            test.assertEqual(asset.basename, test.file_name)
            test.assertEqual(asset.title, Asset.infer_title(test.file_name))
            test.assertEqual(asset.file.read(), test.file_contents)
            test.assertEqual(asset.added_by, test.client.logged_in_user)

            test.assertEqual({asset}, set(upload_history.last_upload_assets(test.user)))

    @override_settings(TRIAL_ACCOUNT_STORAGE_LIMIT=1)
    def test_validation_error_when_quota_exceeded(self):
        response = self.client.post(reverse('asset-upload-action'),
                                    {'file': self.file},
                                    HTTP_X_REQUESTED_WITH='XMLHttpRequest')

        self.assertEqual(200, response.status_code)

        self.assertEqual(0, Asset.objects(self.user).count())

        jsonrpc_response = json.loads(response.content)
        self.assertIn('error', jsonrpc_response)
        self.assertEqual(1, jsonrpc_response['error']['code'])
        self.assertIn('message', jsonrpc_response['error'])
        self.assertNotIn('result', jsonrpc_response)


class UploadHistoryTests(LoggedInTestCase):
    def setUp(self):
        super(UploadHistoryTests, self).setUp()
        setup_example_files(self)

    def test_visiting_upload_page_starts_new_upload(self):
        """
        Test that when you upload some files, go to the upload page and then
        upload some more files the first and second set of assets end up in
        different Upload batches.
        """

        self.assertFalse(self.user_uploads().exists())

        self.client.post(reverse('asset-upload-action'),
                {'file': [self.file, self.file2]})

        self.assertEqual(1, self.user_uploads().count())

        response = self.client.get(reverse('asset-upload'))
        self.assertEqual(200, response.status_code)

        self.client.post(reverse('asset-upload-action'),
                {'file': [self.file, self.file2, self.file]})

        self.assertEqual(2, self.user_uploads().count())

        last_upload_assets = Asset.objects(self.user).order_by("-id")[:3]

        self.assertEqual(set(last_upload_assets),
                         set(upload_history.last_upload_assets(self.user)))

    def test_last_upload_handles_no_uploads(self):
        user = create_user()
        try:
            upload_history.last_upload(user)
        except IndexError:
            self.fail('Last upload should not have errored')

    def user_uploads(self):
        return Upload.objects.filter(added_by=self.user)

    def test_visiting_upload_page_first_doesnt_error(self):
        response = self.client.get(reverse('asset-upload'))
        self.assertEqual(200, response.status_code)


class SlowUploadHistoryTests(LoggedInTestCase):
    needs_index = True

    def test_last_upload_shows_nothing_with_no_uploads(self):
        user = create_user(account=self.account)
        asset = create_asset(account=self.account, user=user,
                             title='test title')

        response_before = self.client.get(reverse('asset-list'))
        self.assertContains(response_before, asset.title)

        response_after = self.client.get(
            reverse('search'), {'last_upload': True})
        self.assertNotContains(response_after, asset.title)
