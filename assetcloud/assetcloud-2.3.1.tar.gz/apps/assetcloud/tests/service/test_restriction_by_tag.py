# -*- coding: utf-8 -*-
# (c) 2012 Bright Interactive Limited. All rights reserved.
# http://www.bright-interactive.com | info@bright-interactive.com

from assetcloud.models import Asset, ProxyTag, get_user_profile_class
from assetcloud.tests.service.test_search import assets_from_results
from assetcloud.tests.service.utils import create_viewer, create_editor, create_admin
from .utils import TestCase, create_asset, create_account
from django.core.exceptions import ValidationError
from django.core.urlresolvers import reverse
from haystack.query import SearchQuerySet

UserProfile = get_user_profile_class()


class RestrictionRoleTests(TestCase):
    """
    Make sure that only viewer users can have tag restrictions applied to them,
    not admins or editors.
    """

    def test_restrictions_removed_when_viewer_changed_to_editor_or_admin(self):
        for new_role in [UserProfile.ROLE_ADMIN, UserProfile.ROLE_EDITOR]:
            tag_names = ['some-tag', 'other-tag']
            user = create_viewer(tags=tag_names)
            tags = {ProxyTag.objects.get(name=tag_name) for tag_name in tag_names}
            self.assertEqual(tags,
                             set(user.get_profile().visible_tags.all()))

            user.get_profile().update_role(new_role)
            # Need to wrap in list() because empty QuerySet compares not equal
            # to []
            remaining_tags = list(user.get_profile().visible_tags.all())
            self.assertEqual([], remaining_tags,
                msg="Tags were not removed when role changed to %s. Remaining tags: %s." % (new_role, remaining_tags))

    def test_restrictions_not_removed_when_changed_to_viewer(self):
        """
        Make sure that calling update_role(UserProfile.ROLE_VIEWER) doesn't
        remove tags.
        """
        tag_names = ['some-tag', 'other-tag']
        user = create_viewer(tags=tag_names)
        tags = {ProxyTag.objects.get(name=tag_name) for tag_name in tag_names}
        self.assertEqual(tags,
                         set(user.get_profile().visible_tags.all()))

        user.get_profile().update_role(UserProfile.ROLE_VIEWER)
        self.assertEqual(tags,
                         set(user.get_profile().visible_tags.all()))

    def test_cant_create_editor_or_admin_with_restrictions(self):
        tag_names = ['some-tag', 'other-tag']
        for create_method in [create_admin, create_editor]:
            with self.assertRaises(ValidationError):
                create_method(tags=tag_names)


class RestrictionByTagTests(TestCase):
    """
    Make sure that tag restrictions are applied when:
     - showing the assets page
     - calling Asset.objects(user)
    """

    needs_index = True
    tags = ['slow']

    def setUp(self):
        super(RestrictionByTagTests, self).setUp()
        self.tag_a = 'a'
        self.tag_b = 'b'
        self.different_tag = 'd'

        self.account = create_account()

        # Note: editors and admins can't have tag restrictions.
        # RestrictionRoleTests makes sure of that, so this test doesn't have to
        # concern itself with what happens when you try to add tags to editors
        # or admins.
        self.editor = create_editor(account=self.account)
        self.account_admin = create_admin(account=self.account)

        self.viewer_a = create_viewer(account=self.account, tags=[self.tag_a])
        self.viewer_b = create_viewer(account=self.account, tags=[self.tag_b])
        self.viewer_both = create_viewer(account=self.account,
                                     tags=[self.tag_a, self.tag_b])
        self.untagged_viewer = create_viewer(account=self.account)

        self.asset_a = create_asset(account=self.account, tags=[self.tag_a])
        self.asset_b = create_asset(account=self.account, tags=[self.tag_b])
        self.asset_both = create_asset(account=self.account,
                                       tags=[self.tag_a, self.tag_b])
        self.different_asset = create_asset(account=self.account,
                                            tags=[self.different_tag])
        self.all_assets = [self.asset_a, self.asset_b,
                           self.asset_both, self.different_asset]

    def test_with_any_tag_for_single_asset_single_user(self):
        expected_assets = [self.asset_a, self.asset_both]
        self.assertCorrectRestrictions(self.viewer_a, expected_assets)

    def test_with_any_tag_for_single_asset_multiple_user(self):
        expected_assets = [self.asset_a, self.asset_b, self.asset_both]
        self.assertCorrectRestrictions(self.viewer_both, expected_assets)

    # FJDTODO: I think that this test might not be necessary because it's testing something that test_with_any_tag_for_single_asset_multiple_user also tests. Check with Jordan and maybe delete.
    def test_cannot_see_assets_without_tag(self):
        visible_assets = Asset.objects(self.viewer_both)
        self.assertNotIn(self.different_asset.pk,
                         [a.pk for a in visible_assets])
        self.assertAssetListPageOnlyContains(self.viewer_both, visible_assets)

    def test_can_see_all_assets_for_viewer_without_tag(self):
        expected_assets = [self.asset_a, self.asset_b,
                           self.asset_both, self.different_asset]
        self.assertCorrectRestrictions(self.untagged_viewer, expected_assets)

    def assertCorrectRestrictions(self, viewer, expected_assets):
        self.assertUserOnlySees(viewer, expected_assets)
        self.assertUserOnlySees(self.editor, self.all_assets)
        self.assertUserOnlySees(self.account_admin, self.all_assets)

    def assertUserOnlySees(self, user, expected_assets):
        # Test the Asset model
        self.assertAssetModelOnlyReturns(user, expected_assets)

        # Test the Asset model via a page
        self.assertAssetDetailsOnlyVisibleFor(user, expected_assets)

        # Test the search classes
        self.assertFilteredSearchOnlyContains(expected_assets, user)

        # Test the search via a page
        self.assertAssetListPageOnlyContains(user, expected_assets)

    def assertAssetModelOnlyReturns(self, user, expected_assets):
        self.assertPksEqualIgnoreOrder(expected_assets,
                                       Asset.objects(user))

    def assertAssetDetailsOnlyVisibleFor(self, user, expected_assets):
        self.client.login(user)
        visible_assets = set()
        for asset in self.all_assets:
            path = reverse('asset', kwargs={'id': asset.id})
            response = self.client.get(path, follow=True)
            if response.status_code == 200:
                visible_assets.add(asset)
            elif response.status_code == 403:
                # Forbidden (means user can't see it)
                pass
            else:
                self.fail("Unexpected status code %d" % response.status_code)

        self.assertPksEqualIgnoreOrder(
            expected_assets,
            visible_assets)

    def assertFilteredSearchOnlyContains(self, expected_assets, user):
        self.assertPksEqualIgnoreOrder(
            expected_assets,
            assets_from_results(
                user.get_profile().filter_search(SearchQuerySet())))

    def assertAssetListPageOnlyContains(self, user, expected_assets):
        self.client.login(user)
        response = self.client.get(reverse('asset-list'), follow=True)
        for asset in expected_assets:
            self.assertIn('href="%s"' % asset.get_absolute_url(), response.content)
