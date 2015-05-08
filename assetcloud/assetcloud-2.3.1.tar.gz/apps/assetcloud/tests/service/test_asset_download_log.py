from django.contrib.auth.models import AnonymousUser
from assetcloud.views import shared_asset_download_action
from django.core.urlresolvers import reverse
from django.test.client import RequestFactory
from assetcloud.models import AssetDownloadLog
from assetcloud.sharing import create_share_for_asset
from assetcloud.tests.contract.utils import TNABotContractTest
from assetcloud.tests.service.utils import create_image_asset, create_asset, LoggedInTestCase


class AssetDownloadLogServiceTests(LoggedInTestCase):

    def setUp(self):
        super(AssetDownloadLogServiceTests, self).setUp()
        self.image_asset = create_image_asset(account=self.account)
        self.non_image_asset = create_asset(account=self.account)

    @TNABotContractTest
    def test_asset_download_logs_log_single_asset_downloads(self):

        self.assertEqual(0, AssetDownloadLog.objects.count())

        self.client.get(
            reverse(
                "asset-download-action",
                kwargs={
                    "id": self.image_asset.id
                }
            )
        )

        self.assertEqual(1, AssetDownloadLog.objects.count())

        download_log = AssetDownloadLog.objects.get()

        self.assertEqual(download_log.asset, self.image_asset)
        self.assertEqual(download_log.user, self.user)

    def test_asset_download_logs_log_shared_asset_downloads(self):
        share = create_share_for_asset(self.image_asset)

        self.assertEqual(0, AssetDownloadLog.objects.count())

        request_factory = RequestFactory()

        anonymous_request = request_factory.get(
            reverse(
                'shared_asset_download_action',
                kwargs={
                    "share_id": share.id,
                    "key": share.key,
                    "asset_id": self.image_asset.id
                }
            )
        )

        anonymous_request.user = AnonymousUser()

        shared_asset_download_action(
            request=anonymous_request,
            share_id=share.id,
            key=share.key,
            asset_id=self.image_asset.id
        )

        self.assertEqual(1, AssetDownloadLog.objects.count())

        download_log = AssetDownloadLog.objects.get()

        self.assertEqual(download_log.asset, self.image_asset)
        self.assertIsNone(download_log.user)

    def test_asset_download_logs_log_resized_asset_downloads(self):

        self.assertEqual(0, AssetDownloadLog.objects.count())

        self.client.get(reverse("asset-resize-base-download-action", kwargs={"id": self.image_asset.id}))
        self.client.get(reverse("asset-resize-download-width-action", kwargs={"id": self.image_asset.id, "width": 10}))
        self.client.get(reverse("asset-resize-download-action", kwargs={"id": self.image_asset.id, "width": 10, "height": 10}))

        self.assertEqual(3, AssetDownloadLog.objects.count())

        download_logs = AssetDownloadLog.objects.all()

        for log in download_logs:
            self.assertEqual(log.asset, self.image_asset)
            self.assertEqual(log.user, self.user)

    @TNABotContractTest
    def test_asset_download_logs_bulk_downloads_as_separate_asset_downloads(self):

        self.assertEqual(0, AssetDownloadLog.objects.count())

        asset_ids = [self.image_asset.id, self.non_image_asset.id]

        self.client.post(
            reverse("prepare_zip_action"),
            data={
                "asset_ids": asset_ids
            }
        )

        self.assertEqual(2, AssetDownloadLog.objects.count())

        download_logs = AssetDownloadLog.objects.order_by("asset__id").all()
        self.assertEqual(download_logs[0].asset, self.image_asset)
        self.assertEqual(download_logs[0].user, self.user)
        self.assertEqual(download_logs[1].asset, self.non_image_asset)
        self.assertEqual(download_logs[1].user, self.user)
