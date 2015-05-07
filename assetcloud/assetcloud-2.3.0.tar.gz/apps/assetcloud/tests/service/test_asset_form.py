from bs4 import BeautifulSoup
from django.core.urlresolvers import reverse
from django.test.utils import override_settings
from sorl.thumbnail.shortcuts import get_thumbnail
from assetcloud.models import Asset
from assetcloud.tests.contract.utils import TNABotContractTest
from assetcloud.tests.service.utils import AdminLoggedInTestCase, create_image_asset, create_image_asset_with_thumbnail


class AssetFormTests(AdminLoggedInTestCase):

    @TNABotContractTest
    def test_form_shows_thumbnail_field(self):
        asset = create_image_asset(account=self.user.get_profile().account)
        response = self.client.get(reverse("asset", kwargs={"id": asset.id}))
        self.assertContains(response=response, text="id=\"id_thumbnail\"")

    @TNABotContractTest
    def test_form_is_displayed_in_asset_page(self):
        asset = create_image_asset(account=self.user.get_profile().account)
        response = self.client.get(reverse("asset", kwargs={"id": asset.id}))
        soup = BeautifulSoup(response.content)
        asset_forms = soup.select("form[action=\"%s\"]" % reverse("asset-update-action", kwargs={"id": asset.id}))
        self.assertEqual(1, len(asset_forms), "Asset form is not in page")

    @TNABotContractTest
    def test_form_is_multipart(self):
        asset = create_image_asset(account=self.user.get_profile().account)
        response = self.client.get(reverse("asset", kwargs={"id": asset.id}))
        soup = BeautifulSoup(response.content)
        asset_form = soup.select("form[action=\"%s\"]" % reverse("asset-update-action", kwargs={"id": asset.id}))[0]
        self.assertEqual("multipart/form-data", asset_form["enctype"])

    @override_settings(ASSET_FILE_STORAGE='django.core.files.storage.FileSystemStorage')
    def test_view_asset_displays_form_with_thumbnail_preview(self):
        asset = create_image_asset_with_thumbnail(account=self.account)

        response = self.client.post(reverse('asset', kwargs={'id': asset.id}))
        soup = BeautifulSoup(response.content)

        current_image_preview = soup.select("fieldset.edit-asset-details .current-image")[0]
        link_to_full_size_image = current_image_preview.select("a")[0]
        preview_image = current_image_preview.select("img")[0]
        self.assertImagePathsEqual(asset.thumbnail.url, link_to_full_size_image["href"])

        thumbnail_preview = get_thumbnail(asset.thumbnail, "150x60")
        self.assertImagePathsEqual(thumbnail_preview.url, preview_image["src"])

    @TNABotContractTest
    def test_form_can_clear_thumbnail(self):
        asset = create_image_asset_with_thumbnail(account=self.user.get_profile().account)
        data = asset.__dict__
        del data["thumbnail"]
        data['thumbnail-clear'] = True
        self.client.post(reverse("asset-update-action", kwargs={"id": asset.id}), data)

        reloaded_asset = Asset.unrestricted_objects.get(id=asset.id)
        self.assertFalse(reloaded_asset.thumbnail)
