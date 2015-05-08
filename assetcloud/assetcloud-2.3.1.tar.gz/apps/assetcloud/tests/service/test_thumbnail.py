# (c) 2011 Bright Interactive Limited. All rights reserved.
# http://www.bright-interactive.com | info@bright-interactive.com

from django.template import Context, Template
from sorl.thumbnail.shortcuts import get_thumbnail
from assetcloud.tests.contract.utils import TNABotContractTest
from assetcloud.tests.service.utils import create_asset, create_image_asset_with_thumbnail
from assetcloud.tests.unit.utils import OverrideAssetcloudSettings
from .utils import list_media_files, TestCase,\
    create_image_asset, create_text_asset


class ThumbnailTests(TestCase):
    """
    Check thumbnail creation and deletion.
    """

    def test_display_thumbnail(self):
        """
        Tests that thumbnails from image assets are generated.
        """
        asset = create_image_asset()

        # Ensure that we can generate a thumbnail URL for the asset.
        template = Template("""
            {% load thumbnail %}
            {% thumbnail asset.file "110x110" crop="center" as image %}
              {{ image.url }}
            {% endthumbnail %}""")
        context = Context({"asset": asset})
        url = template.render(context).strip()
        self.assertTrue(url)

        # Check that the thumbnail image can be downloaded.
        response = self.client.get(url)
        self.assertEquals(response.status_code, 200)
        self.assertEquals(response['Content-Type'], 'image/jpeg')
        self.assertTrue(len(response.content) > 0)

    @TNABotContractTest
    def test_display_large_image_using_tag(self):

        asset = create_image_asset()

        template = Template("""
            {% load asset_large_image %}
            {% asset_large_image asset "300x300" %}""")
        context = Context({"asset": asset})
        rendered_result = template.render(context)
        thumb = get_thumbnail(asset.file, "300x300")
        self.assertIn(thumb.url, str(rendered_result))

    @TNABotContractTest
    def test_display_large_image_using_tag_and_asset_has_thumbnail_displays_large_image(self):

        asset = create_image_asset_with_thumbnail()

        template = Template("""
            {% load asset_large_image %}
            {% asset_large_image asset "300x300" %}""")
        context = Context({"asset": asset})
        rendered_result = template.render(context)
        thumb = get_thumbnail(asset.file, "300x300")
        self.assertIn(thumb.url, str(rendered_result))

    def test_asset_thumbnail_tag_deprecated_but_working(self):

        asset = create_image_asset_with_thumbnail()

        template = Template("""
            {% load asset_thumbnail %}
            {% asset_thumbnail asset "300x300" %}""")
        context = Context({"asset": asset})
        rendered_result = template.render(context)
        thumb = get_thumbnail(asset.file, "300x300")
        self.assertIn(thumb.url, str(rendered_result))

    def test_thumbnails_get_cleaned_up(self):
        """
        Ensure that thumbnails are cleaned up from the cache when the asset
        is deleted.
        """
        # Count the files in the cache
        initial_count = len(list_media_files('cache'))

        # Check that there is one file in the cache dir after creation
        asset = create_image_asset()
        self.assertEquals(len(list_media_files('cache')), initial_count + 1)

        # Check that there are no files in the cache dir after deletion
        asset.delete()
        self.assertEquals(len(list_media_files('cache')), initial_count)

    def test_display_thumbnail_for_image_asset(self):
        """
        Ensure that display_thumbnail returns True for image assets.
        """
        asset = create_image_asset()
        self.assertEqual(True, asset.display_thumbnail)

    @OverrideAssetcloudSettings(
        DEFAULT_LIST_THUMBNAIL_OPTIONS={
            'geometry_string': '300x250',
            'crop': 'center'
        })
    @TNABotContractTest
    def test_display_thumbnail_for_image_asset_respects_settings_changes(self):
        asset = create_image_asset()
        thumbnail = asset.get_list_thumbnail()
        self.assertEqual(300, thumbnail.width)
        self.assertEqual(250, thumbnail.height)

    def test_dont_display_thumbnail_for_text_asset(self):
        """
        Ensure that display_thumbnail returns False for text assets.
        """
        asset = create_text_asset()
        self.assertEqual(False, asset.display_thumbnail)

    def test_dont_display_thumbnail_for_tiff_asset(self):
        asset = create_asset(filename="file.tiff")
        self.assertEqual(False, asset.display_thumbnail)

    def test_dont_display_thumbnail_for_TIFF_asset(self):
        asset = create_asset(filename="file.TIFF")
        self.assertEqual(False, asset.display_thumbnail)

    def test_dont_display_thumbnail_for_tif_asset(self):
        asset = create_asset(filename="file.tif")
        self.assertEqual(False, asset.display_thumbnail)

    def test_dont_display_thumbnail_for_TIF_asset(self):
        asset = create_asset(filename="file.TIF")
        self.assertEqual(False, asset.display_thumbnail)

    def test_dont_display_thumbnail_for_psd_asset(self):
        asset = create_asset(filename="file.psd")
        self.assertEqual(False, asset.display_thumbnail)

    def test_dont_display_thumbnail_for_PSD_asset(self):
        asset = create_asset(filename="file.PSD")
        self.assertEqual(False, asset.display_thumbnail)
