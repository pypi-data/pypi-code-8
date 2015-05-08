# (c) 2011 Bright Interactive Limited. All rights reserved.
# http://www.bright-interactive.com | info@bright-interactive.com
from bs4 import BeautifulSoup
from sorl.thumbnail.shortcuts import get_thumbnail
from assetcloud import random_utils
from assetcloud.models import Asset
from assetcloud.random_utils import random_image_file
from assetcloud.storage import S3BotoStorage
from assetcloud.tests.contract.utils import TNABotContractTest
from assetcloud.tests.service.test_search import search_results
from assetcloud.tests.service.utils import create_account, create_user, \
    create_editor, create_asset, list_media_files, TestCase, RoleTest, \
    LoggedInTestCase, create_image_asset_with_thumbnail
from assetcloud.tests.test_models.models import TestAssetMetadataModel, AnotherTestAssetMetadataModel
from assetcloud.tests.unit.utils import OverrideAssetcloudSettings
from assetcloud.upload_history import upload_asset
from django.core.files import File
from django.utils.html import escape
from django.core.urlresolvers import reverse
from assetcloud import app_settings as assetcloud_settings


class AssetTests(TestCase):
    """
    Tests that make sure that things can be done programmatically using a
    sensible interface.
    """

    def test_default_filename(self):
        file = random_utils.random_file_obj()
        asset = Asset(file=File(file, name='foobar.dat'))
        self.assertEqual(asset.filename, 'foobar.dat')

    def test_default_filename_path_stripped(self):
        file = random_utils.random_file_obj()
        asset = Asset(file=File(file, name='/foo/bar/baz.dat'))
        self.assertEqual(asset.filename, 'baz.dat')

    def test_overridden_filename(self):
        file = random_utils.random_file_obj()
        asset = Asset(file=File(file, name='foobar.dat'),
                      filename='overridden.dat')
        self.assertEqual(asset.filename, 'overridden.dat')

    def test_create_asset(self):
        file = random_utils.random_file_obj()
        user = create_user()
        asset = Asset(file=File(file, name='foobar.dat'),
                      added_by=user, account=user.get_profile().account)
        upload_asset(asset, added_by=user)

        # Reload the asset...
        reloaded_asset = Asset.unrestricted_objects.get(id=asset.id)

        # ...and check that it's details and contents have been persisted.
        self.assertEqual(file.size, reloaded_asset.file.size)
        self.assertEqual(file.size, reloaded_asset.file_size)
        self.assertEqual('foobar.dat', reloaded_asset.basename)
        self.assertEqual(
            file.getvalue(),
            reloaded_asset.file.read())

    def test_create_asset_with_thumbnail_creates_asset_with_thumbnail(self):
        asset = create_image_asset_with_thumbnail()
        asset = Asset.unrestricted_objects.get(id=asset.id)
        self.assertIsNotNone(asset.thumbnail)

    def test_delete_asset_with_thumbnail_deletes_thumbnail_too(self):
        asset = create_image_asset_with_thumbnail()
        thumb = asset.thumbnail
        self.assertTrue(thumb.storage.exists(thumb.name))
        asset.delete()
        self.assertFalse(thumb.storage.exists(thumb.name))

    def test_replacing_asset_thumbnail_deletes_original_thumbnail(self):
        asset = create_image_asset_with_thumbnail()
        old_thumb = asset.thumbnail
        self.assertTrue(old_thumb.storage.exists(old_thumb.name))
        asset.thumbnail = File(
            random_utils.random_image_file(
                None, '.png'))
        asset.save()
        new_thumb = asset.thumbnail
        self.assertTrue(new_thumb.storage.exists(new_thumb.name))
        self.assertFalse(old_thumb.storage.exists(old_thumb.name))

    def test_file_size_updated(self):
        file = random_utils.random_file_obj(content_length=321)
        user = create_user()
        asset = Asset(file=File(file, name='foobar.dat'),
                      added_by=user, account=user.get_profile().account)
        upload_asset(asset, added_by=user)

        self.assertEqual(321, asset.file_size)

        reloaded_asset = Asset.unrestricted_objects.get(id=asset.id)
        self.assertEqual(321, reloaded_asset.file_size)
        del reloaded_asset

        # Test updating file via original asset instance
        file = random_utils.random_file_obj(content_length=456)
        asset.file = File(file, name='foobar.dat')
        asset.save()
        self.assertEqual(456, asset.file_size)
        reloaded_asset = Asset.unrestricted_objects.get(id=asset.id)
        self.assertEqual(456, reloaded_asset.file_size)

        del asset

        # Test updating file via reloaded asset instance
        file = random_utils.random_file_obj(content_length=789)
        reloaded_asset.file = File(file, name='foobar.dat')
        reloaded_asset.save()
        self.assertEqual(789, reloaded_asset.file_size)
        reloaded_asset = Asset.unrestricted_objects.get(id=reloaded_asset.id)
        self.assertEqual(789, reloaded_asset.file_size)

    def test_doesnt_hit_s3_when_updating_asset_metadata(self):
        # Monkey patch call counting on to S3BotoStorage. I tried sublassing it
        # and using
        # @override_settings(ASSET_FILE_STORAGE = 'assetcloud.tests.service.assets.InstrumentedS3BotoStorage')
        # but that didn't work, I suspect because the storage was instantiated
        # before the @override_settings decorator ran.
        AssetTests.size_call_count = 0
        original_size = S3BotoStorage.size

        def instrumented_size(self, name):
            AssetTests.size_call_count += 1
            return original_size(self, name)
        S3BotoStorage.size = instrumented_size

        asset = create_asset()

        call_count_before = AssetTests.size_call_count
        asset.file.size
        call_count_after = AssetTests.size_call_count
        # Check that call count has increased - if not there's a problem with
        # the test and the main test below probably won't actually be testing
        # anything useful.
        self.assertGreater(call_count_after, call_count_before)

        call_count_before = AssetTests.size_call_count
        asset.description = 'other'
        asset.save()
        call_count_after = AssetTests.size_call_count
        self.assertEqual(call_count_after, call_count_before)

    def test_delete_asset(self):
        asset = create_asset()

        asset.delete()

        self.assertRaises(Asset.DoesNotExist, Asset.unrestricted_objects.get,
                          id=asset.id)

    @TNABotContractTest
    def test_asset_list_thumbnail_defaults_to_explicit_thumbnail_if_exists(self):
        asset = create_image_asset_with_thumbnail()
        thumbnail_from_asset = asset.get_list_thumbnail()

        thumbnail_from_asset_file = get_thumbnail(
            asset.file,
            **assetcloud_settings.DEFAULT_LIST_THUMBNAIL_OPTIONS
        )

        thumbnail_from_asset_thumbnail = get_thumbnail(
            asset.thumbnail,
            **assetcloud_settings.DEFAULT_LIST_THUMBNAIL_OPTIONS
        )

        self.assertImagePathsEqual(thumbnail_from_asset.url, thumbnail_from_asset_thumbnail.url)
        self.assertImagePathsNotEqual(thumbnail_from_asset.url, thumbnail_from_asset_file.url)


class AssetFieldTests(TestCase):
    def test_description_is_saved(self):
        description = ("I'm a little teapot, short and stout, "
                       "pick me up and pour me out.")
        asset = create_asset(description=description)

        reloaded_asset = Asset.unrestricted_objects.get(id=asset.id)
        del asset

        self.assertEqual(description, reloaded_asset.description)


class BasicNonImageAssetTests(TestCase):
    def test_non_image_asset_deletes_okay(self):
        """
        Ensure that a non image asset can be deleted without error.
        """
        # Check that there are no files in the cache dir,
        # when the asset exists.
        asset = create_asset()
        self.assertEqual(len(list_media_files('cache')), 0)

        # Check that there are no files in the cache dir,
        # when the asset has been deleted.
        asset.delete()
        self.assertEqual(len(list_media_files('cache')), 0)

    def test_non_image_asset_returns_display_thumnbail_true_if_it_has_an_explicit_thumbnail(self):
        asset = create_asset()
        asset.thumbnail = "some/image/path.jpg"
        asset.save()

        self.assertTrue(asset.display_thumbnail)


class ListAssetsTests(LoggedInTestCase):
    needs_index = True

    def test_title_html_escaped(self):
        account = self.user.get_profile().account

        title = "Ev<il> title"
        escaped_title = "Ev&lt;il&gt; title"
        create_asset(title=title, account=account)

        response = self.client.get(reverse('asset-list'))

        self.assertEqual(response.status_code, 200)
        # Check that the HTML contains the escaped title
        self.assertContains(response, escaped_title)
        # Check that the HTML does not contain the raw un-escaped title
        self.assertNotContains(response, title)


class SlowListAssetsTests(LoggedInTestCase):
    tags = ['slow']
    needs_index = True

    def test_asset_list_contains_assets(self):
        """
        Tests that the list asset page contains all the assets.

        """

        account = self.user.get_profile().account
        create_asset(account=account)
        create_asset(account=account)

        # Get the set of all the assets
        assets = set(Asset.objects(self.user).account(account))

        # Get the asset list page
        response = self.client.get(reverse('asset-list'))

        # Ensure all the page is rendered with the correct template,
        # and the correct list of assets.
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'assetcloud/pages/search.html')
        # Compare as sets instead of lists because we only want to check that
        # they contain the same assets, not the order that the assets appear
        # in.
        self.assertSetEqual(set(search_results(response)),
                            assets)

    def test_asset_list_recently_added_assets_are_displayed_first(self):
        account = self.user.get_profile().account
        asset_1 = create_asset(account=account)
        asset_2 = create_asset(account=account)
        asset_3 = create_asset(account=account)

        expected = [asset_3, asset_2, asset_1]

        response = self.client.get(reverse('asset-list'))

        self.assertListEqual(expected, list(search_results(response)))


class ViewAssetTests(LoggedInTestCase):
    def setUp(self):
        super(ViewAssetTests, self).setUp()

    def get_asset_response(self, id):
        return self.client.get(reverse('asset', kwargs={'id': id}))

    def test_view_asset(self):
        asset = create_asset(account=self.account)

        response = self.get_asset_response(asset.id)

        # Ensure all the page is rendered with the correct template,
        # and the correct asset.
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'assetcloud/pages/asset.html')
        self.assertEqual(asset, response.context['asset'])

    def test_filename_on_page(self):
        asset = create_asset(account=self.account)
        response = self.get_asset_response(asset.id)
        self.assertContains(response, '<strong>%s</strong> uploaded' % escape(asset.filename))

    def test_view_non_existent_asset(self):
        # id of the asset to use for testing (must not exist).
        asset_id = 42

        response = self.get_asset_response(asset_id)

        # Ensure we get a 404 not found status code back.
        self.assertEqual(response.status_code, 404)

    def test_cant_view_other_accounts_asset(self):
        other_account = create_account()
        other_account_user = create_user(account=other_account)

        asset = create_asset(account=self.account)

        self.client.login(other_account_user)

        response = self.get_asset_response(asset.id)

        # Ensure that we get a permission denied page.
        self.assertEqual(response.status_code, 403)

    @OverrideAssetcloudSettings(
        ASSET_METADATA_MODELS=[
            "test_models.TestAssetMetadataModel",
            "test_models.AnotherTestAssetMetadataModel"
        ]
    )
    def test_view_asset_displays_additional_fields_when_extended(self):
        asset = create_asset(account=self.account)
        metadata = TestAssetMetadataModel(asset=asset)
        metadata.required_field = "Required field value"
        metadata.non_required_field = "Non-required field value"

        more_metadata = AnotherTestAssetMetadataModel(asset=asset)

        more_metadata.another_required_field = "Another required field value"
        more_metadata.another_non_required_field = "Another non-required field value"

        metadata.save()
        more_metadata.save()

        response = self.get_asset_response(asset.id)

        soup = BeautifulSoup(response.content)
        asset_metadata = soup.select(".content")[0]

        self.assertIn("Required field value", str(asset_metadata))
        self.assertIn("Non-required field value", str(asset_metadata))
        self.assertIn("Another required field value", str(asset_metadata))
        self.assertIn("Another non-required field value", str(asset_metadata))

    @OverrideAssetcloudSettings(
        ASSET_METADATA_MODELS=[
            "test_models.TestAssetMetadataModel",
            "test_models.AnotherTestAssetMetadataModel"
        ]
    )
    def test_view_asset_displays_placeholders_when_no_metadata_is_defined(self):
        asset = create_asset(account=self.account)
        metadata = TestAssetMetadataModel(asset=asset)
        metadata.required_field = "Required field value"
        metadata.non_required_field = "Non-required field value"

        metadata.save()

        response = self.get_asset_response(asset.id)

        soup = BeautifulSoup(response.content)
        asset_metadata = soup.select(".metadata")[0]

        metadata_placeholders = asset_metadata.select("td.placeholder")

        self.assertIn("Required field value", str(asset_metadata))
        self.assertIn("Non-required field value", str(asset_metadata))
        self.assertEqual(2, len(metadata_placeholders))

    @OverrideAssetcloudSettings(
        ASSET_METADATA_MODELS=[
            "test_models.TestAssetMetadataModel",
        ]
    )
    def test_view_asset_displays_form_if_error_in_metadata_on_submit(self):
        asset = create_asset(account=self.account)

        data = asset.__dict__
        del data["thumbnail"]
        del data['_original_thumbnail']

        response = self.client.post(reverse('asset-update-action', kwargs={'id': asset.id}), data=data)

        soup = BeautifulSoup(response.content)

        # The form is visible if the container div has .click-to-edit and edit classes
        form_visible = soup.select("div.click-to-edit.edit")
        self.assertEqual(1, len(form_visible))
        self.assertIn("This field is required", str(soup))


class UpdateAssetPageTests(LoggedInTestCase):
    def setUp(self):
        super(UpdateAssetPageTests, self).setUp()
        account = create_account()
        self.user = create_user(account=account)
        self.client.login(self.user)

    def test_form_variable_available_to_template(self):
        account = self.user.get_profile().account
        asset = create_asset(account=account)

        url = reverse('asset', kwargs={"id": asset.id})
        response = self.client.get(url)

        # Ensure all the page is rendered with the correct template,
        # and the correct asset.
        self.assertEqual(response.status_code, 200)
        self.assertIsNotNone(response.context['form'])
        self.assertEqual(asset, response.context['form'].instance)

    class RoleTestUpdateAssetTitle(RoleTest):
        can = ['editor', 'admin']

        @OverrideAssetcloudSettings(ASSET_METADATA_MODELS=[])
        def when(self, test):
            # Create an asset
            self.asset = create_asset(account=test.account)

            # Setup form
            self.title = random_utils.random_unicode(256)
            form = dict(id=self.asset.id,
                        title=self.title)

            # Submit the form and check the response
            self.view_kwargs = {'id': self.asset.id}
            return test.client.post(reverse('asset-update-action',
                                            kwargs=self.view_kwargs), form)

        @OverrideAssetcloudSettings(ASSET_METADATA_MODELS=[])
        def role_can(self, test, response):
            test.assertRedirects(response, reverse('asset',
                                                   kwargs=self.view_kwargs))

            # Check that the asset has been updated
            reloaded_asset = \
                Asset.unrestricted_objects.get(id=self.asset.id)
            del self.asset
            test.assertEqual(self.title, reloaded_asset.title)

    def test_cant_update_other_accounts_asset(self):
        other_account = create_account()
        other_account_user = create_user(account=other_account)

        old_title = 'Old title'
        asset = create_asset(account=self.user.get_profile().account,
                             title=old_title)

        self.client.login(other_account_user)

        # Setup form
        title = 'New title'
        form = dict(id=asset.id,
                    title=title)

        # Submit the form and check the response
        view_kwargs = {'id': asset.id}
        response = self.client.post(reverse('asset-update-action',
                                            kwargs=view_kwargs), form)

        # Ensure that we get a permission denied page.
        self.assertEqual(response.status_code, 403)

        # Check that the asset has NOT been updated
        reloaded_asset = Asset.objects(self.user).get(id=asset.id)
        del asset
        self.assertEqual(old_title, reloaded_asset.title)

    class RoleTestUpdateThumbnail(RoleTest):
        can = ['editor', 'admin']

        @TNABotContractTest
        @OverrideAssetcloudSettings(ASSET_METADATA_MODELS=[])
        def when(self, test):
            self.asset = create_asset(account=test.account)
            test.assertFalse(self.asset.thumbnail)
            self.thumb = File(random_image_file())

            data = {
                "id": self.asset.id,
                'thumbnail': self.thumb
            }
            return test.client.post(reverse("asset-update-action", kwargs={"id": self.asset.id}), data)

        @TNABotContractTest
        @OverrideAssetcloudSettings(ASSET_METADATA_MODELS=[])
        def role_can(self, test, response):
            test.assertRedirects(response, reverse('asset', kwargs={"id": self.asset.id}))
            updated_asset = Asset.unrestricted_objects.get(id=self.asset.id)
            test.assertIsNotNone(updated_asset.thumbnail.url)


def _delete_asset_test_setup(self, user):
    self.asset = create_asset(account=self.user.get_profile().account)
    self.form = dict(id=self.asset.id)
    self.kwargs = dict(id=self.asset.id)


class DeleteAssetRoleTests(TestCase):

    class RoleTestDeleteAsset(RoleTest):
        can = ['editor', 'admin']

        def given(self, test):
            _delete_asset_test_setup(test, test.user)

        def when(self, test):
            return test.client.post(reverse('asset-delete-action',
                                            kwargs=test.kwargs),
                                    test.form)

        def role_can(self, test, response):
            response = test.client.get(reverse('asset', kwargs=test.kwargs))
            test.assertEqual(response.status_code, 404)


class DeleteAssetTests(TestCase):
    def setUp(self):
        super(DeleteAssetTests, self).setUp()

        self.user = create_editor()
        _delete_asset_test_setup(self, self.user)

        self.client.login(self.asset.added_by)

    def test_asset_delete_action_deletes_asset(self):
        self.client.post(reverse('asset-delete-action', kwargs=self.kwargs),
                         self.form)

        # The deleted asset cannot be viewed
        response = self.client.get(reverse('asset', kwargs=self.kwargs))
        self.assertEqual(response.status_code, 404)

    def test_asset_delete_action_redirects_to_asset_list_page(self):
        response = self.client.post(reverse('asset-delete-action',
                                            kwargs=self.kwargs), self.form)

        self.assertRedirects(response, reverse('asset-list'))

    def test_asset_delete_action_with_non_existent_asset_id(self):
        self.kwargs = dict(id=self.asset.id + 1)

        response = self.client.post(reverse('asset-delete-action',
                                            kwargs=self.kwargs), self.form)

        self.assertEqual(response.status_code, 404)

    def test_asset_delete_action_user_who_did_not_create_asset_can_still_delete_it(self):
        account = self.asset.account
        user = create_user(account=account, is_editor=True)
        self.client.login(user)

        self.client.post(reverse('asset-delete-action', kwargs=self.kwargs), self.form)

        # The deleted asset cannot be viewed
        response = self.client.get(reverse('asset', kwargs=self.kwargs))
        self.assertEqual(response.status_code, 404)

    def test_asset_delete_action_with_user_from_different_account_returns_403(self):
        other_user = create_user(account=create_account())
        self.client.login(other_user)

        response = self.client.post(reverse('asset-delete-action',
                                            kwargs=self.kwargs), self.form)

        self.assertEqual(response.status_code, 403)

    def test_asset_delete_action_with_user_from_different_account_asset_is_not_deleted(self):
        other_user = create_user(account=create_account())
        self.client.login(other_user)

        self.client.post(reverse('asset-delete-action',
                                 kwargs=self.kwargs), self.form)

        reloaded_asset = Asset.objects(self.user).get(id=self.asset.id)
        self.assertEqual(self.asset.id, reloaded_asset.id)
