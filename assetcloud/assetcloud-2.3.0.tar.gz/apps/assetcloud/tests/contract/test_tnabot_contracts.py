import datetime
from django.template.base import Template
from django.template.context import Context
from django.http import QueryDict
from assetcloud.tests.contract.service_utils import LoggedInContractTestCase
from assetcloud.tests.service.utils import create_image_asset, create_asset, create_fake_request
from assetcloud.tests.contract.utils import ContractTestCase
from assetcloud.models import Asset
from assetcloud.views import AddToFolderAction


class TNABoTContractTests(ContractTestCase):

    def test_extended_templates_exist(self):
        self.assertTemplateExists("assetcloud/pages/logged_out/base.html")
        self.assertTemplateExists("assetcloud/snippets/asset_display_thumbnail.html")
        self.assertTemplateExists("assetcloud/pages/logged_out/login.html")

    def test_used_blocks_exist(self):
        self.assertBlockInTemplate("title", "assetcloud/pages/logged_out/base.html")
        self.assertBlockInTemplate("box_content", "assetcloud/pages/logged_out/base.html")
        self.assertBlockInTemplate("body", "assetcloud/pages/logged_out/base.html")
        self.assertBlockInTemplate("body-attr", "assetcloud/pages/logged_out/base.html")
        self.assertBlockInTemplate("page_scripts", "assetcloud/pages/logged_out/base.html")

    def test_variables_exist_in_overridden_template_views(self):
        self.assertVariableInViewContext("fade_class", "login")

    def test_used_urls_exists(self):
        self.assertUrlExists("forgotten-password")
        self.assertUrlExists("login")
        self.assertUrlExists("logout")

    def test_imports_are_valid(self):
        self.assertValidImport("assetcloud.models.BaseUserProfile")
        self.assertValidImport("assetcloud_auth.forms.LoginForm")
        self.assertValidImport("assetcloud.models.Asset")
        self.assertValidImport("assetcloud.models.Account")
        self.assertValidImport("assetcloud.tests.service.utils.SuperAdminLoggedInTestCase")
        self.assertValidImport("assetcloud.tests.service.utils.AdminLoggedInTestCase")
        self.assertValidImport("assetcloud.tests.service.utils.LoggedInTestCase")
        self.assertValidImport("assetcloud.tests.service.utils.ViewerLoggedInTestCase")
        self.assertValidImport("assetcloud.tests.service.utils.RoleTest")
        self.assertValidImport("assetcloud.tests.service.utils.TestCase")
        self.assertValidImport("assetcloud.tests.service.utils.create_account")
        self.assertValidImport("assetcloud.tests.service.utils.create_asset")
        self.assertValidImport("assetcloud.tests.service.utils.create_user")
        self.assertValidImport("assetcloud.tests.service.utils.get_last_added_user")
        self.assertValidImport("assetcloud.asset_metadata_util.get_metadata_model_and_form_classes")
        self.assertValidImport("assetcloud.random_utils.random_alphanumeric")
        self.assertValidImport("assetcloud_auth.emailcase")
        self.assertValidImport("assetcloud.views.decorators.public")
        self.assertValidImport("assetcloud.views.decorators.public")

    def test_asset_display_thumbnail_template_displays_thumbnail(self):
        asset = create_image_asset()
        template = Template("{% include 'assetcloud/snippets/asset_display_thumbnail.html' %}")
        context = Context({"asset": asset})

        rendered_template = template.render(context=context)
        self.assertIn('alt="%s"' % asset.title, rendered_template)

    def test_asset_fields(self):
        now = datetime.datetime.now()
        asset = create_asset(
            title='test title', filename='test filename', added=now)
        self.assertEqual('test title', asset.title)
        self.assertEqual('test filename', asset.filename)
        self.assertEqual(asset.added, now)

    def test_asset_display_thumbnail(self):
        asset = create_image_asset()
        self.assertTrue(
            Asset.unrestricted_objects.get(pk=asset.pk).display_thumbnail)
        asset.image_info.delete()
        self.assertFalse(
            Asset.unrestricted_objects.get(pk=asset.pk).display_thumbnail)


class TNABoTLoggedInContractTests(LoggedInContractTestCase):
    def test_add_to_folder_action_returns_response_from_process_ids(self):
        class FakeAddToFolderAction(AddToFolderAction):
            def process_ids(self, *args, **kwargs):
                super(FakeAddToFolderAction, self).process_ids(*args, **kwargs)
                return 10
        asset = create_image_asset()
        request = create_fake_request(user=self.user)
        request.POST = QueryDict('asset_ids=%s' % asset.pk)
        self.assertEqual(
            10,
            FakeAddToFolderAction().post(
                request, folder_id=self.user.get_profile().folder.pk))

    def test_remove_from_folder_action_returns_response_from_process_ids(self):
        class FakeRemoveFromFolderAction(AddToFolderAction):
            def process_ids(self, *args, **kwargs):
                super(FakeRemoveFromFolderAction, self).process_ids(*args, **kwargs)
                return 10
        asset = create_image_asset()
        request = create_fake_request(user=self.user)
        request.POST = QueryDict('asset_ids=%s' % asset.pk)
        self.assertEqual(
            10,
            FakeRemoveFromFolderAction().post(
                request, folder_id=self.user.get_profile().folder.pk))
