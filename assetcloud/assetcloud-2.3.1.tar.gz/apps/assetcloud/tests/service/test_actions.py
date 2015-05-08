from assetcloud.models import Asset
from assetcloud.tests.service.utils import RoleTest, create_editor
from assetcloud.tests.contract.utils import TNABotContractTest
from .utils import LoggedInTestCase, create_asset, create_account, create_admin, create_viewer, with_delete_zf
from django.core.urlresolvers import reverse
from django.http import QueryDict
from assetcloud.views import get_asset_ids_from_request, InvalidAssetIdsError
import zipfile
import os
from StringIO import StringIO
from email.utils import quote


def make_asset_ids(*assets):
    return {'asset_ids': ",".join(str(a.id) for a in assets)}


class ActionsSearchPageTests(LoggedInTestCase):
    needs_index = True

    def test_search_results_show_select_bar(self):
        create_asset(account=self.account)
        self.assertIn('select-bar',
                      self.client.get(reverse('home')).content)


class ActionsTests(LoggedInTestCase):
    def create_request(self, string):
        req = lambda: None
        req.POST = QueryDict("asset_ids=%s" % (string or ''))
        return req

    @TNABotContractTest
    def test_get_asset_ids(self):
        request = self.create_request("1,2,3,4")
        self.assertEqual([1, 2, 3, 4], get_asset_ids_from_request(request))

    @TNABotContractTest
    def test_get_asset_ids_with_multiples(self):
        request = self.create_request("1,2,3,4,3,2")
        self.assertEqual([1, 2, 3, 4, 3, 2], get_asset_ids_from_request(request))

    @TNABotContractTest
    def test_get_asset_ids_with_invalid_characters(self):
        request = self.create_request("1,invalidlistm3,3")
        self.assertRaises(InvalidAssetIdsError, get_asset_ids_from_request, request)

    @TNABotContractTest
    def test_get_asset_ids_with_blank(self):
        request = self.create_request("")
        self.assertEqual([], get_asset_ids_from_request(request))

    @TNABotContractTest
    def test_get_asset_ids_with_null(self):
        request = self.create_request(None)
        self.assertEqual([], get_asset_ids_from_request(request))

    @TNABotContractTest
    def test_get_asset_ids_with_empty_get(self):
        request = self.create_request(None)
        request.POST = QueryDict('')
        self.assertEqual([], get_asset_ids_from_request(request))

    @TNABotContractTest
    def test_get_asset_ids_allows_list(self):
        request = self.create_request(None)
        request.POST = QueryDict('asset_ids=1&asset_ids=2')
        self.assertEqual([1, 2], get_asset_ids_from_request(request))


class DownloadZipActionTestCase(LoggedInTestCase):
    """
    Base class for tests of zip download actions.

    Contains utility methods and tests that should pass for all zip download
    actions - these tests will be run once for each subclass.
    """
    def setUp(self):
        super(DownloadZipActionTestCase, self).setUp()
        self.asset1 = create_asset(account=self.account)
        self.asset2 = create_asset(account=self.account)
        self.assets = [self.asset1, self.asset2]
        self.folder = self.user.get_profile().folder

    def get_zipfile(self):
        return zipfile.ZipFile(self.client.session['zip_file'])

    def prepare_and_download_zip(self, *args, **kwargs):
        self.post_prepare(*args, **kwargs)
        response = self.get_download_zip()
        content = self.unstream_content(response.streaming_content)
        return zipfile.ZipFile(StringIO(content))

    def unstream_content(self, streaming_content):
        """
        Convert streaming_content, an iterable of byte strings, into a single
        byte string.
        """
        content = b''.join(streaming_content)
        return content

    def prepare_and_get_zipfile(self):
        self.post_prepare()
        return self.get_zipfile()

    def prepare_and_get_zip_filenames(self):
        zf = self.prepare_and_get_zipfile()
        filenames = zf.namelist()
        return filenames

    def assertZipContains(self, *assets, **kwargs):
        if 'zf' in kwargs:
            zf = kwargs['zf']
        else:
            zf = self.get_zipfile()
        names = zf.namelist()
        asset_names = [a.filename for a in assets]
        for name in names:
            self.assertIn(name, asset_names)


class CommonDownloadZipActionTestsMixin(object):
    @TNABotContractTest
    @with_delete_zf
    def test_prepare_zip_sets_session_variable(self):
        self.post_prepare()
        self.assertTrue(self.client.session['zip_file'])

    @TNABotContractTest
    @with_delete_zf
    def test_prepare_zip_prepares_zip(self):
        zf = self.prepare_and_get_zipfile()
        self.assertIsNone(zf.testzip())

    @TNABotContractTest
    @with_delete_zf
    def test_download_as_zip_contains_expected_files(self):
        zf = self.prepare_and_download_zip()
        for name in zf.namelist():
            f = zf.read(name)
            for asset in self.assets:
                if asset.filename == name:
                    self.assertEqual(f, asset.file.read())


class SlowCommonDownloadZipActionTestsMixin(object):

    @TNABotContractTest
    @with_delete_zf
    def test_prepare_zip_uses_asset_filename(self):
        asset_filenames = [a.filename for a in self.assets]
        zip_filenames = self.prepare_and_get_zip_filenames()
        for name in zip_filenames:
            self.assertIn(name, asset_filenames)

    @TNABotContractTest
    def test_download_as_zip_deletes_session_zip(self):
        self.post_prepare()
        path = self.client.session['zip_file']
        self.assertTrue(os.path.exists(path))
        try:
            response = self.get_download_zip()
            response.close()  # Django normally calls this
            self.assertFalse(os.path.exists(path))
        finally:
            if os.path.exists(path):
                os.remove(path)

    @TNABotContractTest
    @with_delete_zf
    def test_download_as_zip_respects_restrictions(self):
        visible_asset = self.asset1
        invisible_asset = self.asset2

        visible_asset.tags.add('visible')
        invisible_asset.tags.add('invisible')

        viewer = create_viewer(account=self.account)
        viewer.get_profile().visible_tags.add('visible')
        admin = create_admin(account=self.account)

        self.client.login(admin)
        zf = self.prepare_and_download_zip()
        self.assertZipContains(visible_asset, invisible_asset, zf=zf)

        self.client.login(viewer)
        zf = self.prepare_and_download_zip()
        self.assertZipContains(visible_asset, zf=zf)

    @TNABotContractTest
    @with_delete_zf
    def test_download_as_zip_sets_content_disposition(self):
        self.post_prepare()
        response = self.get_download_zip()
        self.assertEquals(response['Content-Disposition'],
                          'attachment; filename="%s"' %
                          quote(response.filename))


class DownloadSelectedZipActionTestCase(DownloadZipActionTestCase):
    """
    Tests specific to downloading selected assets.
    """

    def post_prepare(self, assets=None):
        if assets is None:
            assets = self.assets
        url = reverse('prepare_zip_action')
        self.client.post(url, data=make_asset_ids(*assets))

    def get_download_zip(self):
        url = reverse('download_zip_action')
        return self.client.get(url)

    def prepare_and_download_zip(self, assets=None):
        if not assets:
            assets = self.assets
        return super(DownloadSelectedZipActionTestCase, self).prepare_and_download_zip(assets=assets)


class DownloadSelectedZipActionTests(DownloadSelectedZipActionTestCase, CommonDownloadZipActionTestsMixin):

    @TNABotContractTest
    @with_delete_zf
    def test_prepare_zip_with_no_ids(self):
        url = reverse('prepare_zip_action')
        response = self.client.post(url, data={'asset_ids': ""})
        self.assertEqual(response.status_code, 403)
        self.assertIsNone(self.client.session.get('zip_file'))

    @TNABotContractTest
    @with_delete_zf
    def test_download_as_zip_respects_account(self):
        other_asset = create_asset(account=create_account())
        zf = self.prepare_and_download_zip(assets=[self.asset1,
                                                   self.asset2,
                                                   other_asset])
        self.assertZipContains(self.asset1, self.asset2, zf=zf)


class SlowDownloadSelectedZipActionTestCase(DownloadSelectedZipActionTestCase, SlowCommonDownloadZipActionTestsMixin):
    pass


class DownloadFolderZipActionTestCase(DownloadZipActionTestCase):
    needs_index = True

    def setUp(self):
        super(DownloadFolderZipActionTestCase, self).setUp()
        self.folder.assets.add(self.asset1)
        self.folder.assets.add(self.asset2)

        self.asset_not_in_folder = create_asset(account=self.account)

    def post_prepare(self, assets=None):
        url = reverse('prepare_folder_zip_action')
        self.client.post(url)

    def get_download_zip(self):
        url = reverse('download_zip_action')
        return self.client.get(url)


class DownloadFolderZipActionTests(DownloadFolderZipActionTestCase, CommonDownloadZipActionTestsMixin):

    @TNABotContractTest
    @with_delete_zf
    def test_asset_not_in_folder_not_in_zip(self):
        zip_filenames = self.prepare_and_get_zip_filenames()
        self.assertNotIn(self.asset_not_in_folder.filename, zip_filenames)
        folder_filenames = {a.filename for a in self.folder.assets.all()}
        self.assertSetEqual(folder_filenames, set(zip_filenames))


class SlowDownloadFolderZipActionTestCase(DownloadFolderZipActionTestCase, SlowCommonDownloadZipActionTestsMixin):
    pass


class DeleteAssetsActionTests(LoggedInTestCase):
    def test_delete_multiple_assets(self):
        account = self.user.get_profile().account
        asset1 = create_asset(account=account)
        asset2 = create_asset(account=account)
        asset3 = create_asset(account=account)

        self.client.post(
            reverse('delete_assets_action'),
            data=make_asset_ids(asset1, asset2, asset3)
        )

        self.assertEquals(0, len(Asset.objects(self.user).all()))


class SlowDeleteAssetsActionTests(LoggedInTestCase):
    tags = ['slow']

    class RoleTestDeleteAssets(RoleTest):
        can = ['editor', 'admin']
        cant = ['viewer']

        def when(self, test):
            self.asset1 = create_asset(account=test.account)
            self.asset2 = create_asset(account=test.account)
            self.asset3 = create_asset(account=test.account)

            test.assertEquals(3, len(Asset.objects(test.user).all()))

            url = reverse('delete_assets_action')
            data = make_asset_ids(self.asset1, self.asset2, self.asset3)

            return test.client.post(url, data=data)

        def role_can(self, test, response):
            test.assertEquals(0, len(Asset.objects(test.user).all()))

    def test_delete_asset_where_assets_belong_to_a_different_account(self):
        account = self.user.get_profile().account
        asset1 = create_asset(account=account)
        asset2 = create_asset(account=account)

        other_account = create_account(name="Other Account")
        other_editor_user = create_editor(account=other_account)
        other_asset1 = create_asset(account=other_account)
        other_asset2 = create_asset(account=other_account)
        other_asset3 = create_asset(account=other_account)

        self.assertEquals(2, len(Asset.objects(self.user).all()))
        self.assertEquals(3, len(Asset.objects(other_editor_user).all()))

        self.client.post(
            reverse('delete_assets_action'),
            data=make_asset_ids(asset1, asset2, other_asset1, other_asset2, other_asset3)
        )

        self.assertEquals(0, len(Asset.objects(self.user).all()))
        # The other account's assets have not been deleted
        self.assertEquals(3, len(Asset.objects(other_editor_user).all()))

    def test_delete_with_null_asset_ids(self):
        response = self.client.post(
            reverse('delete_assets_action'),
            data={'asset_ids': None}
        )
        self.assertEqual(response.status_code, 403)

    def test_delete_with_no_asset_ids(self):
        response = self.client.post(
            reverse('delete_assets_action')
        )
        self.assertEqual(response.status_code, 403)

    def test_delete_with_invalid_asset_ids(self):
        response = self.client.post(
            reverse('delete_assets_action'),
            data={'asset_ids': 'notreal1,notreal2'}
        )
        self.assertEqual(response.status_code, 403)

    class RoleTestViewDeleteButton(RoleTest):
        can = ['editor', 'admin']
        cant = ['viewer']

        def when(self, test):
            create_asset(account=test.account)
            return test.client.get(reverse('home'))

        def role_can(self, test, response):
            test.assertContains(response, 'href="#delete-modal')

        def assertCant(self, role_name, test, response):
            test.assertNotContains(response, 'href="#delete-modal')
