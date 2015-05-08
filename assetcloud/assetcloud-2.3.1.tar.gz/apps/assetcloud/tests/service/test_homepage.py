from django.core.urlresolvers import reverse
from assetcloud.random_utils import random_alphanumeric
from assetcloud.tests.unit.utils import OverrideAssetcloudSettings
from .utils import LoggedInTestCase, create_asset
from assetcloud.models import Asset


class HomepageTestCase(LoggedInTestCase):
    def get_homepage(self):
        return self.client.get(reverse('home'))


class HomepageTests(HomepageTestCase):
    def test_home_page_has_no_filters(self):
        response = self.get_homepage()
        self.assertNotContains(response, 'Filters', status_code=200)

    def test_home_page_has_highlighted_link(self):
        response = self.get_homepage()
        self.assertContains(response, 'home active arrow_box">')


class SlowHomepageTests(HomepageTestCase):
    tags = ['slow']
    needs_index = True

    def create_test_assets(self, **kwargs):
        for i in range(3):
            create_asset(account=self.account, title="asset_%s" % i, **kwargs)

    def get_assets_in_descending_date_order(self):
        return Asset.objects(self.user).order_by('-added')

    @OverrideAssetcloudSettings(HOMEPAGE_TAG_MAX_ASSET_COUNT=2)
    def test_home_page_serves_2_recently_added_assets(self):
        self.create_test_assets()
        assets = self.get_assets_in_descending_date_order()
        response = self.get_homepage()

        for asset in assets[:2]:
            self.assertContains(response, asset.title)
        self.assertNotContains(response, assets[2].title)
        self.assertBulkActionsShown(response)

    def assertBulkActionsShown(self, response):
        self.assertTemplateUsed(response, 'assetcloud/snippets/actions.html')

    @OverrideAssetcloudSettings(HOMEPAGE_TAG_MAX_ASSET_COUNT=2)
    def test_homepage_displays_2_tagged_assets(self):
        test_tag_name = random_alphanumeric()
        self.create_test_assets(tags=[test_tag_name])
        # Reverse as homepage tags display assets oldest->newest
        assets = list(reversed(self.get_assets_in_descending_date_order()))

        # Need to push assets 19 and 20 off the recently added list
        for i in range(3):
            create_asset(account=self.account, title="assets_%s")
        response = self.get_homepage()

        expected_asset = assets[1]
        unexpected_asset = assets[0]
        self.assertNotContains(response, expected_asset.title)
        self.assertNotContains(response, unexpected_asset.title)

        self.account.homepage_tags.add(test_tag_name)

        response = self.get_homepage()
        self.assertContains(response, expected_asset.title)
        self.assertNotContains(response, unexpected_asset.title)

    def test_homepage_does_not_display_tags_with_no_assets(self):
        test_tag_name = random_alphanumeric
        self.account.homepage_tags.add(test_tag_name)
        response = self.get_homepage()
        self.assertNotContains(response, test_tag_name)
