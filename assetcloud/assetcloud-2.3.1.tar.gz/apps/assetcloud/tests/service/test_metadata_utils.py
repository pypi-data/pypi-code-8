from django.core.exceptions import ObjectDoesNotExist
from django.forms.models import ModelForm
from django.test.testcases import TestCase

from assetcloud.asset_metadata_util import get_class_from_string, metadata_form, get_metadata_model_and_form_classes, get_asset_metadata_for_metadata_model, get_asset_metadata, \
    BaseMetadataModel
from assetcloud.tests.contract.utils import TNABotContractTest
from assetcloud.tests.service.utils import create_asset
from assetcloud.tests.test_models.forms import ExtensionModelForm
from assetcloud.tests.test_models.models import TestAssetMetadataModel, AnotherTestAssetMetadataModel, TestModel, MetadataModelWithManyToMany
from assetcloud.tests.unit.utils import OverrideAssetcloudSettings


class TestClass():
    pass


class AssetMetadataUtilTests(TestCase):

    def test_can_get_class_from_string(self):
        cls = get_class_from_string("assetcloud.tests.service.test_metadata_utils.TestClass")
        self.assertEqual(cls, TestClass)

    def test_metadata_form_is_a_model_form(self):
        form_class = metadata_form(TestAssetMetadataModel)
        self.assertTrue(issubclass(form_class, ModelForm))

    def test_metadata_form_has_the_correct_meta_model(self):
        form_class = metadata_form(TestAssetMetadataModel)
        self.assertEqual(form_class.Meta.model, TestAssetMetadataModel)

    def test_get_metadata_classes_gets_correct_classes_if_no_form_is_defined(self):
        metadata_model, metadata_form = get_metadata_model_and_form_classes("test_models.TestAssetMetadataModel")
        self.assertEqual(metadata_model, TestAssetMetadataModel)
        self.assertEqual(metadata_form.Meta.model, TestAssetMetadataModel)

    @TNABotContractTest
    def test_get_metadata_classes_gets_correct_classes_if_form_is_defined(self):
        metadata_model, metadata_form = get_metadata_model_and_form_classes(
            ("test_models.TestAssetMetadataModel", "assetcloud.tests.test_models.forms.ExtensionModelForm")
        )
        self.assertEqual(metadata_model, TestAssetMetadataModel)
        self.assertEqual(metadata_form, ExtensionModelForm)

    @OverrideAssetcloudSettings(ASSET_METADATA_MODELS=["test_models.TestAssetMetadataModel"])
    def test_get_metadata_for_metadata_model_returns_correct_model(self):
        asset = create_asset()

        asset_metadata = TestAssetMetadataModel(asset=asset)
        asset_metadata.required_field = "some data"
        asset_metadata.non_required_field = "some other data"
        asset_metadata.save()

        retrieved_metadata = get_asset_metadata_for_metadata_model(asset, TestAssetMetadataModel)
        self.assertEqual(asset_metadata, retrieved_metadata)

    @OverrideAssetcloudSettings(ASSET_METADATA_MODELS=[
        "test_models.TestAssetMetadataModel",
        "test_models.AnotherTestAssetMetadataModel"
    ])
    def test_get_all_asset_metadata_returns_all_metadata(self):
        asset = create_asset()

        asset_metadata = TestAssetMetadataModel(asset=asset)
        asset_metadata.required_field = "some data"
        asset_metadata.non_required_field = "some other data"
        asset_metadata.save()

        other_asset_metadata = AnotherTestAssetMetadataModel(asset=asset)
        other_asset_metadata.another_required_field = "some data"
        other_asset_metadata.another_non_required_field = "some other data"
        other_asset_metadata.save()

        retrieved_metadata = get_asset_metadata(asset)
        self.assertEqual(4, len(retrieved_metadata))
        self.assertInMetadata(retrieved_metadata, label="required field", value="some data", name="required_field")
        self.assertInMetadata(retrieved_metadata, label="non required field", value="some other data", name="non_required_field")
        self.assertInMetadata(retrieved_metadata, label="another required field", value="some data", name="another_required_field")
        self.assertInMetadata(retrieved_metadata, label="another non required field", value="some other data", name="another_non_required_field")

    @OverrideAssetcloudSettings(ASSET_METADATA_MODELS=["test_models.MetadataModelWithManyToMany"])
    def test_get_metadata_for_metadata_model_supports_many_to_many_fields(self):
        asset = create_asset()

        asset_metadata = MetadataModelWithManyToMany(asset=asset)
        asset_metadata.save()
        test_1 = TestModel.objects.create(name="test 1")
        test_2 = TestModel.objects.create(name="test 2")
        test_3 = TestModel.objects.create(name="test 3")

        asset_metadata.tests.add(test_1)
        asset_metadata.tests.add(test_2)
        asset_metadata.tests.add(test_3)

        retrieved_metadata = get_asset_metadata(asset)
        self.assertInMetadata(retrieved_metadata, name="tests", label="tests", value="test 1, test 2, test 3")

    def assertInMetadata(self, metadata, label, value, name):

        found = False

        for attribute in metadata:
            if attribute["label"] == label and attribute["value"] == value and attribute["name"] == name:
                found = True

        self.assertTrue(found, "Metadata %s, %s, %s was not in received metadata" % (label, value, name))

    @OverrideAssetcloudSettings(ASSET_METADATA_MODELS=[
        "test_models.TestAssetMetadataModel",
        "test_models.CreateOnSaveMetadataModel"
    ])
    @TNABotContractTest
    def test_asset_metadata_gets_created_on_save_if_they_have_create_on_save_meta_set(self):
        asset = create_asset()

        with self.assertRaises(ObjectDoesNotExist):
            asset.metadata
        try:
            asset.create_on_save_metadata
        except ObjectDoesNotExist:
            self.fail('Metadata with create on save meta should be created on save')

    @TNABotContractTest
    def test_classes_extending_base_metadata_have_create_on_save_meta_attribute(self):
        class MetadataModel(BaseMetadataModel):
            pass

        self.assertTrue(hasattr(MetadataModel._metadata_meta, 'create_on_save'))

    def test_classes_extending_base_metadata_have_create_on_save_meta_attribute_default_to_false(self):
        class MetadataModel(BaseMetadataModel):
            pass

        self.assertFalse(MetadataModel._metadata_meta.create_on_save)

    @TNABotContractTest
    def test_classes_extending_base_metadata_can_override_create_on_save(self):
        class MetadataModel(BaseMetadataModel):
            class MetadataMeta:
                create_on_save = True

        self.assertTrue(MetadataModel._metadata_meta.create_on_save)
