from .test_search import search_results
from .utils import TestCase, LoggedInTestCase, RoleTest, create_account, create_asset, create_user, create_viewer, create_admin, create_editor
from assetcloud.models import Folder, get_user_profile_class
from bs4 import BeautifulSoup
from django.core.urlresolvers import reverse
import re
from assetcloud.tests.contract.utils import TNABotContractTest

UserProfile = get_user_profile_class()


class FolderTests(TestCase):
    def setUp(self):
        super(FolderTests, self).setUp()
        self.user = create_editor()
        self.account = self.user.get_profile().account

    def test_nav_link_is_called_favourites(self):
        self.create_editor_and_login()
        response = self.client.get(reverse('home'))
        response_soup = BeautifulSoup(response.content)
        folder_link = response_soup.find('a', href=reverse("favourites"))
        self.assertEqual('favourites', folder_link.text)

    @TNABotContractTest
    def test_new_users_get_default_folder(self):
        user = UserProfile._create_user(account=create_account())
        self.assertTrue(user.folders.exists())

    @TNABotContractTest
    def test_create_default_folder_creates_default_folder(self):
        folder = Folder.create_default_folder(self.user)
        self.assertEqual(folder.name, 'Favourites')
        self.assertEqual(folder.owner, self.user)

    @TNABotContractTest
    def test_folder_property_returns_folder(self):
        self.assertEqual(self.user.folders.get(),
                         self.user.get_profile().folder)

    @TNABotContractTest
    def test_contains_works(self):
        folder = self.user.get_profile().folder
        asset1, asset2 = (create_asset(account=self.account),
                          create_asset(account=self.account))
        self.assertFalse(folder.contains(asset1))
        self.assertFalse(folder.contains(asset2))
        folder.assets.add(asset1)
        self.assertTrue(folder.contains(asset1))
        self.assertFalse(folder.contains(asset2))
        folder.assets.add(asset2)
        self.assertTrue(folder.contains(asset1))
        self.assertTrue(folder.contains(asset2))


class ViewFolderSetup(object):
    def set_up_folders(self):
        self.asset1, self.asset2 = (create_asset(account=self.account),
                                    create_asset(account=self.account))
        folder = self.user.get_profile().folder
        folder.assets.add(self.asset1)
        folder.assets.add(self.asset2)


class ViewFolderTests(LoggedInTestCase, ViewFolderSetup):
    """
    Tests to do with viewing the contents of folders.
    """
    needs_index = True

    def setUp(self):
        super(ViewFolderTests, self).setUp()
        self.set_up_folders()

    def test_view_folder_page_shows_assets_in_favourites(self):
        expected = set((self.asset1, self.asset2))

        response = self.client.get(reverse('favourites'))
        self.assertTemplateUsed(response, 'assetcloud/pages/search.html')
        self.assertSetEqual(expected,
                            set(search_results(response)))

    def test_view_folder_page_doesnt_show_restricted_assets(self):
        expected = set([self.asset1])
        self.asset1.tags.add('cansee')
        self.asset2.tags.add('cantsee')

        self.user = create_viewer(account=self.account)
        self.client.login(self.user)
        self.user.get_profile().visible_tags.add('cansee')

        folder = self.user.get_profile().folder
        folder.assets.add(self.asset1)
        folder.assets.add(self.asset2)

        response = self.client.get(reverse('favourites'))
        self.assertSetEqual(expected, set(search_results(response)))


class SlowViewFolderTests(LoggedInTestCase, ViewFolderSetup):
    tags = ['slow']
    needs_index = True

    def setUp(self):
        super(SlowViewFolderTests, self).setUp()
        self.set_up_folders()

    def test_view_folder_page_doesnt_show_asset_not_in_favourites(self):
        expected = set((self.asset1, self.asset2))

        # Create another asset that is NOT in the user's folder
        create_asset(account=self.account)

        response = self.client.get(reverse('favourites'))
        self.assertTemplateUsed(response, 'assetcloud/pages/search.html')
        self.assertSetEqual(expected, set(search_results(response)))

    def test_folders_param_doesnt_show_other_folders(self):
        other_admin = create_admin(account=self.account)
        other_asset = create_asset(account=self.account)
        other_admin.get_profile().folder.assets.add(other_asset)
        # If searching for the folder directly returns all of the assets
        # instead of just the one in the folder, the test passes
        expected = set([self.asset1, self.asset2, other_asset])
        response = self.client.get(
            reverse("search") + '?folders=%s' % other_admin.get_profile().folder.pk)
        self.assertEqual(expected, set(search_results(response)))

    def test_view_folder_page_shows_download_all_link(self):
        response = self.client.get(reverse('favourites'))

        self.assertEqual(200, response.status_code)
        found = self._download_all_link_in_response(response)
        self.assertTrue(found, msg='Download All link not found')

    def test_search_page_does_not_show_download_all_link(self):
        response = self.client.get(reverse('search'))

        self.assertEqual(200, response.status_code)
        found = self._download_all_link_in_response(response)
        self.assertFalse(found, msg="Download All link found on search page - it shouldn't be there because it will download the folder contents, not the search results")

    def _download_all_link_in_response(self, response):
        response_soup = BeautifulSoup(response.content)
        download_re = re.compile('.*Download all.*', re.DOTALL)
        # This doesn't find the link, don't know why, so we have to do it the long way
        #link = response_soup.find('a', text=download_re)
        #self.assertIsNotNone(link, msg='Download All link not found')
        found = False
        for l in response_soup.find_all('a'):
            if download_re.match(l.text):
                found = True
                break
        return found


class AssetFolderPageTests(LoggedInTestCase):
    def setUp(self):
        super(AssetFolderPageTests, self).setUp()
        self.asset_in_folder = create_asset(account=self.account)
        self.asset_not_in_folder = create_asset(account=self.account)
        self.user.get_profile().folder.assets.add(self.asset_in_folder)

    def test_asset_page_shows_add_to_favourites(self):
        self.assertResponseContains('Add to favourites',
                                    self.client.get(
                reverse('asset',
                        kwargs=dict(id=self.asset_not_in_folder.pk))))

    def test_asset_page_shows_remove_from_favourites(self):
        self.assertResponseContains('Remove from favourites',
                                    self.client.get(
                reverse('asset',
                        kwargs=dict(id=self.asset_in_folder.pk))))


class FolderTestCase(LoggedInTestCase):
    def setUp(self):
        super(FolderTestCase, self).setUp()
        self.folder = self.user.get_profile().folder
        self.asset1 = create_asset(account=self.account)
        self.asset2 = create_asset(account=self.account)

    def make_post_data(self, *assets):
        return {'asset_ids': ",".join(str(a.id) for a in assets)}


class AddToFolderTests(FolderTestCase):
    class RoleTestAddToFolder(RoleTest):
        can = ['viewer', 'admin', 'editor']

        def when(self, test):
            self.folder = test.user.get_profile().folder
            asset1 = create_asset(account=test.account)
            asset2 = create_asset(account=test.account)
            url = reverse('add_to_folder_action', kwargs={
                    'folder_id': self.folder.pk
                    })
            return test.client.post(url, data=test.make_post_data(asset1,
                                                                  asset2))

        def role_can(self, test, response):
            test.assertEqual(self.folder.assets.count(), 2)

    @TNABotContractTest
    def test_add_to_folder_respects_owner(self):
        user = create_user(account=self.account)
        target_folder = user.get_profile().folder

        response = self.client.post(reverse('add_to_folder_action',
                                            kwargs={
                    'folder_id': target_folder.pk
                    }), data=self.make_post_data(self.asset1, self.asset2))

        self.assertFalse(target_folder.assets.exists())
        self.assertEqual(response.status_code, 403)

    @TNABotContractTest
    def test_add_to_folder_respects_account(self):
        target_folder = self.folder
        asset1 = create_asset(account=create_account())
        asset2 = create_asset(account=create_account())

        self.client.post(reverse('add_to_folder_action',
                                            kwargs={
                    'folder_id': target_folder.pk
                    }), data=self.make_post_data(asset1, asset2))
        self.assertFalse(target_folder.assets.exists())

    @TNABotContractTest
    def test_add_to_folder_respects_asset_restrictions(self):
        restricted_asset = create_asset(account=self.account, tags=['restrict'])
        visible_asset = create_asset(account=self.account, tags=['not_restrict'])

        viewer = create_viewer(account=self.account)
        viewer.get_profile().visible_tags.add('not_restrict')

        admin_folder = self.folder
        viewer_folder = viewer.get_profile().folder

        data = self.make_post_data(restricted_asset, visible_asset)

        self.client.post(reverse('add_to_folder_action',
                                            kwargs={
                    'folder_id': admin_folder.pk
                    }), data=data)
        self.assertTrue(admin_folder.contains(restricted_asset))
        self.assertTrue(admin_folder.contains(visible_asset))

        self.client.login(viewer)

        self.client.post(reverse('add_to_folder_action',
                                            kwargs={
                    'folder_id': viewer_folder.pk
                    }), data=data)
        self.assertFalse(viewer_folder.contains(restricted_asset))
        self.assertTrue(viewer_folder.contains(visible_asset))

    @TNABotContractTest
    def test_asset_cannot_be_added_twice(self):
        asset = create_asset(account=self.account)

        self.client.post(reverse('add_to_folder_action',
                                            kwargs={
                    'folder_id': self.folder.pk
                    }), data=self.make_post_data(asset, asset))
        self.assertEqual(self.folder.assets.count(), 1)

        self.client.post(reverse('add_to_folder_action',
                                            kwargs={
                    'folder_id': self.folder.pk
                    }), data=self.make_post_data(asset, asset))
        self.assertEqual(self.folder.assets.count(), 1)

    @TNABotContractTest
    def test_add_with_empty_param(self):
        response = self.client.post(reverse('add_to_folder_action',
                                            kwargs={
                    'folder_id': self.folder.pk
                    }), data={'asset_ids': ''})
        self.assertEqual(response.status_code, 403)

    @TNABotContractTest
    def test_add_with_null_param(self):
        response = self.client.post(reverse('add_to_folder_action',
                                            kwargs={
                    'folder_id': self.folder.pk
                    }), data={'asset_ids': None})
        self.assertEqual(response.status_code, 403)

    @TNABotContractTest
    def test_add_with_no_param(self):
        response = self.client.post(reverse('add_to_folder_action',
                                            kwargs={
                    'folder_id': self.folder.pk
                    }))
        self.assertEqual(response.status_code, 403)

    @TNABotContractTest
    def test_add_with_invalid_param(self):
        response = self.client.post(reverse('add_to_folder_action',
                                            kwargs={
                    'folder_id': self.folder.pk
                    }), data={'asset_ids': 'notreal'})
        self.assertEqual(response.status_code, 403)


class RemoveFromFolderTests(FolderTestCase):
    class RoleTestRemoveFromFolder(RoleTest):
        can = ['viewer', 'admin', 'editor']

        def when(self, test):
            self.folder = test.user.get_profile().folder
            asset1 = create_asset(account=test.account)
            asset2 = create_asset(account=test.account)
            self.folder.assets.add(asset1, asset2)

            url = reverse('remove_from_folder_action', kwargs={
                    'folder_id': self.folder.pk
                    })
            return test.client.post(url, data=test.make_post_data(asset1,
                                                                  asset2))

        def role_can(self, test, response):
            test.assertFalse(self.folder.assets.exists())

    @TNABotContractTest
    def test_remove_from_folder_respects_owner(self):
        user = create_user(account=self.account)
        target_folder = user.get_profile().folder
        target_folder.assets.add(self.asset1, self.asset2)

        self.client.post(
            reverse('remove_from_folder_action',
                    kwargs={
                    'folder_id': target_folder.pk
                    }),
            data=self.make_post_data(self.asset1, self.asset2))

        self.assertEqual(target_folder.assets.count(), 2)

    @TNABotContractTest
    def test_remove_from_folder_respects_asset_restrictions(self):
        restricted_asset = create_asset(account=self.account, tags=['restrict'])
        visible_asset = create_asset(account=self.account, tags=['not_restrict'])

        viewer = create_viewer(account=self.account)
        viewer.get_profile().visible_tags.add('not_restrict')

        admin_folder = self.folder
        viewer_folder = viewer.get_profile().folder

        data = self.make_post_data(restricted_asset, visible_asset)
        admin_folder.assets.add(restricted_asset, visible_asset)
        viewer_folder.assets.add(restricted_asset, visible_asset)

        self.client.post(
            reverse('remove_from_folder_action',
                    kwargs={
                    'folder_id': admin_folder.pk
                    }),
            data=data)
        self.assertFalse(admin_folder.contains(restricted_asset))
        self.assertFalse(admin_folder.contains(visible_asset))

        self.client.login(viewer)

        self.assertTrue(viewer_folder.contains(restricted_asset))
        self.client.post(
            reverse('remove_from_folder_action',
                    kwargs={
                    'folder_id': viewer_folder.pk
                    }),
            data=data)
        self.assertTrue(viewer_folder.contains(restricted_asset))
        self.assertFalse(viewer_folder.contains(visible_asset))

    @TNABotContractTest
    def test_asset_cannot_be_removed_twice(self):
        asset = create_asset(account=self.account)
        self.folder.assets.add(asset)

        self.client.post(
            reverse('remove_from_folder_action',
                    kwargs={
                    'folder_id': self.folder.pk
                    }),
            data=self.make_post_data(asset, asset))
        self.assertEqual(self.folder.assets.count(), 0)

        self.client.post(
            reverse('remove_from_folder_action',
                    kwargs={
                    'folder_id': self.folder.pk
                    }),
            data=self.make_post_data(asset, asset))
        self.assertEqual(self.folder.assets.count(), 0)

    @TNABotContractTest
    def test_remove_with_empty_param(self):
        response = self.client.post(
            reverse('remove_from_folder_action',
                    kwargs={
                    'folder_id': self.folder.pk
                    }),
            data={'asset_ids': ''})
        self.assertEqual(response.status_code, 403)

    @TNABotContractTest
    def test_remove_with_null_param(self):
        response = self.client.post(
            reverse('remove_from_folder_action',
                    kwargs={
                    'folder_id': self.folder.pk
                    }),
            data={'asset_ids': None})
        self.assertEqual(response.status_code, 403)

    @TNABotContractTest
    def test_remove_with_no_param(self):
        response = self.client.post(
            reverse('remove_from_folder_action',
                    kwargs={
                    'folder_id': self.folder.pk
                    }))
        self.assertEqual(response.status_code, 403)

    @TNABotContractTest
    def test_remove_with_invalid_param(self):
        response = self.client.post(
            reverse('remove_from_folder_action',
                    kwargs={
                    'folder_id': self.folder.pk
                    }),
            data={'asset_ids': 'notreal'})
        self.assertEqual(response.status_code, 403)
