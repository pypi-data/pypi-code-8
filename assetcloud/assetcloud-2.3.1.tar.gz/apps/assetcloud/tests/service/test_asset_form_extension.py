from assetcloud.asset_metadata_util import metadata_form
from assetcloud.forms import AssetForm
from assetcloud.models import Asset
from assetcloud.tests.contract.utils import TNABotContractTest
from assetcloud.tests.service.utils import TestCase, create_asset
from assetcloud.tests.test_models.forms import ExtensionModelForm
from assetcloud.tests.test_models.models import TestAssetMetadataModel
from assetcloud.tests.unit.utils import OverrideAssetcloudSettings


class AssetFormExtensionTests(TestCase):

    @TNABotContractTest
    def test_can_create_dynamic_modelform(self):

        form = metadata_form(TestAssetMetadataModel)()

        self.assertEqual(form.Meta.model, TestAssetMetadataModel)

    @TNABotContractTest
    @OverrideAssetcloudSettings(ASSET_METADATA_MODELS=["test_models.TestAssetMetadataModel"])
    def test_main_asset_form_is_extended(self):
        form = AssetForm()

        self.assertEqual(1, len(form.metadata_forms))
        self.assertEqual(TestAssetMetadataModel, form.metadata_forms[0].Meta.model)

    @TNABotContractTest
    @OverrideAssetcloudSettings(ASSET_METADATA_MODELS=[])
    def test_main_asset_form_is_valid_when_passing_asset_data(self):
        asset = create_asset()
        form = AssetForm(data=asset.__dict__)
        self.assertTrue(form.is_valid())

    @TNABotContractTest
    @OverrideAssetcloudSettings(ASSET_METADATA_MODELS=["test_models.TestAssetMetadataModel"])
    def test_extended_asset_form_uses_metadata_form_validation(self):
        asset = create_asset()
        form = AssetForm(data=asset.__dict__)
        self.assertFalse(form.is_valid())

    @TNABotContractTest
    @OverrideAssetcloudSettings(ASSET_METADATA_MODELS=["test_models.TestAssetMetadataModel"])
    def test_extended_asset_form_uses_metadata_is_valid_when_metadata_required_fields_are_populated(self):
        asset = create_asset()
        data = asset.__dict__
        data["required_field"] = "some data"
        form = AssetForm(data, instance=asset)
        self.assertTrue(form.is_valid())

    @TNABotContractTest
    @OverrideAssetcloudSettings(ASSET_METADATA_MODELS=["test_models.TestAssetMetadataModel"])
    def test_extended_asset_form_creates_metadata_entry_on_save(self):

        all_metadata = TestAssetMetadataModel.objects.all()
        self.assertEqual(0, len(all_metadata))

        asset = create_asset()
        data = asset.__dict__
        data["required_field"] = "some data"
        form = AssetForm(data, instance=asset)
        form.save()

        all_metadata = TestAssetMetadataModel.objects.all()
        self.assertEqual(1, len(all_metadata))

    @TNABotContractTest
    @OverrideAssetcloudSettings(ASSET_METADATA_MODELS=["test_models.TestAssetMetadataModel"])
    def test_extended_asset_form_associates_metadata_entry_with_asset_on_save(self):

        asset = create_asset()

        asset_metadata = TestAssetMetadataModel.objects.filter(asset=asset)
        self.assertEqual(0, len(asset_metadata))

        data = asset.__dict__
        data["required_field"] = "some data"
        form = AssetForm(data, instance=asset)
        form.save()

        asset_metadata = TestAssetMetadataModel.objects.filter(asset=asset)
        self.assertEqual(1, len(asset_metadata))

    @TNABotContractTest
    @OverrideAssetcloudSettings(ASSET_METADATA_MODELS=["test_models.TestAssetMetadataModel"])
    def test_extended_asset_form_stores_all_metadata_on_save(self):

        asset = create_asset()

        data = asset.__dict__
        data["required_field"] = "some data"
        data["non_required_field"] = "some other data"
        form = AssetForm(data, instance=asset)
        form.save()

        asset_metadata = TestAssetMetadataModel.objects.filter(asset=asset)[0]
        self.assertEqual("some data", asset_metadata.required_field)
        self.assertEqual("some other data", asset_metadata.non_required_field)

    @TNABotContractTest
    @OverrideAssetcloudSettings(ASSET_METADATA_MODELS=["test_models.TestAssetMetadataModel"])
    def test_extended_asset_form_initialises_metadata_on_initialisation_on_edit(self):

        asset = create_asset()
        data = asset.__dict__
        data["required_field"] = "some data"
        data["non_required_field"] = "some other data"
        form = AssetForm(data, instance=asset)
        form.save()

        metadata_instance = TestAssetMetadataModel.objects.get(asset=asset)

        form = AssetForm(instance=asset)

        custom_metadata_form = form.metadata_forms[0]

        self.assertEqual(metadata_instance, custom_metadata_form.instance)

    @OverrideAssetcloudSettings(
        ASSET_METADATA_MODELS=[
            "test_models.TestAssetMetadataModel",
            "test_models.AnotherTestAssetMetadataModel"
        ]
    )
    def test_extended_asset_form_can_handle_more_than_one_metadata_extension(self):

        asset = create_asset()
        data = asset.__dict__
        data["required_field"] = "some data"
        data["non_required_field"] = "some other data"
        data["another_required_field"] = "some data for second model"
        data["another_non_required_field"] = "some other data for second model"
        form = AssetForm(data, instance=asset)
        form.save()

        asset = Asset.unrestricted_objects.get(pk=asset.pk)
        self.assertEqual(asset.metadata.required_field, "some data")
        self.assertEqual(asset.metadata.non_required_field, "some other data")
        self.assertEqual(asset.more_metadata.another_required_field, "some data for second model")
        self.assertEqual(asset.more_metadata.another_non_required_field, "some other data for second model")

    @TNABotContractTest
    @OverrideAssetcloudSettings(
        ASSET_METADATA_MODELS=[
            "test_models.TestAssetMetadataModel",
            (
                "test_models.AnotherTestAssetMetadataModel",
                "assetcloud.tests.test_models.forms.ExtensionModelForm"
            )
        ]
    )
    def test_extended_asset_form_uses_defined_model_form_if_available(self):

        form = AssetForm()
        self.assertEqual(2, len(form.metadata_forms))
        self.assertEqual(ExtensionModelForm, type(form.metadata_forms[1]))
