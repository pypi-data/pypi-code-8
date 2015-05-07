from assetcloud.models import Asset
from assetcloud.tests.contract.utils import TNABotContractTest
from .utils import UnitTestCase


class InferTitleTests(UnitTestCase):
    def assertInferred(self, given, expected):
        self.assertEqual(Asset.infer_title(given), expected)

    def test_infer_title(self):
        self.assertInferred("a.png", "a")
        self.assertInferred("test_file.png", "test_file")
        self.assertInferred("123.15d.png", "123.15d")

    def test_infer_title_without_ext(self):
        self.assertInferred("a", "a")
        self.assertInferred("A123BA2", "A123BA2")

    def test_infer_title_with_only_ext(self):
        self.assertInferred(".png", ".png")
        self.assertInferred(".test", ".test")


class ExplicitThumbnailTests(UnitTestCase):

    @TNABotContractTest
    def test_asset_model_has_thumbnail_field(self):
        try:
            Asset._meta.get_field('thumbnail')
        except AttributeError:
            self.fail("Asset model doesn't have a thumbnail field")

    @TNABotContractTest
    def test_thumbnails_are_optional(self):
        field = Asset._meta.get_field('thumbnail')
        self.assertTrue(field.blank)
        self.assertTrue(field.null)
