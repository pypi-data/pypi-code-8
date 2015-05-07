from assetcloud.sharing import share_asset, create_share_for_asset
from assetcloud.tests.service.utils import get_html_content
from assetcloud.tests.contract.utils import TNABotContractTest
from .utils import LoggedInTestCase
from assetcloud import sharing
from bs4 import BeautifulSoup
from django.core import mail
from django.core.exceptions import PermissionDenied
from django.core.urlresolvers import reverse
from django.contrib.auth.models import User
from django.utils.html import escape
from assetcloud.models import Share, BaseUserProfile
import datetime


class SharingTests(LoggedInTestCase):
    def setUp(self):
        super(SharingTests, self).setUp()
        self.asset = self.create_asset()

    def test_sharing_sends_mail(self):
        self.assertEqual(len(mail.outbox), 0)
        share_asset(self.user,
                    self.asset,
                    'test@example.com',
                    domain='test')
        self.assertEqual(len(mail.outbox), 1)

    def test_sharing_saves_message(self):
        share = share_asset(self.user, self.asset, 'test@example.com',
                            message='Hello World!')
        self.assertEqual('Hello World!', share.message)


class SharingViewTests(LoggedInTestCase):
    def setUp(self):
        super(SharingViewTests, self).setUp()
        self.asset = self.create_asset()

    def test_share_assets_action_sends_mail(self):
        self.assertEqual(len(mail.outbox), 0)

        url = reverse('share_assets_action')
        self.client.post(url, data={
            'asset_ids': self.asset.id,
            'recipient': 'test@example.com',
        })

        self.assertEqual(len(mail.outbox), 1)
        email = mail.outbox[0]

        self.assertEqual(['test@example.com'], email.to)
        # Check that Asset (singular) not Assets (plural) is used
        self.assertIn('asset', email.subject.lower())
        self.assertNotIn('assets', email.subject.lower())
        self.assertIn('asset', email.body.lower())
        self.assertNotIn('assets', email.body.lower())

    @TNABotContractTest
    def test_mail_uses_overridden_from_address(self):
        class SharingUserProfileSubclass(BaseUserProfile):
            @classmethod
            def get_from_address(cls, *args):
                return 'test@test.com'

        class UserSubclass(User):
            def get_profile(self):
                return SharingUserProfileSubclass(user=self)

        sharing.send_sharing_email(UserSubclass(), [], "", "", None, "")
        self.assertEqual('test@test.com', mail.outbox[0].from_email)

    def test_share_assets_action_sends_mail_with_custom_message(self):
        self.assertEqual(len(mail.outbox), 0)

        url = reverse('share_assets_action')
        self.client.post(url, data={
            'asset_ids': self.asset.id,
            'recipient': 'test@example.com',
            'message': '<script>escape me</script>',
        })

        self.assertEqual(len(mail.outbox), 1)
        # Should be escaped in HTML version but not plain text version.
        self.assertIn('&lt;script&gt;escape me&lt;/script&gt;', get_html_content(mail.outbox[0]))
        self.assertIn('<script>escape me</script>', mail.outbox[0].body)

    def test_custom_message_shown_on_share_page(self):
        url = reverse('share_assets_action')
        self.client.post(url, data={
            'asset_ids': self.asset.id,
            'recipient': 'test@example.com',
            'message': '<script>escape me</script>',
        })

        share = Share.objects.order_by('-id')[0]

        response = self.client.get(share.get_absolute_url())
        self.assertContains(response, '&lt;script&gt;escape me&lt;/script&gt;')

    def test_register_link_shown_on_share_page(self):
        url = reverse('share_assets_action')
        self.client.post(url, data={
            'asset_ids': self.asset.id,
            'recipient': 'test@example.com',
            'message': '<script>escape me</script>',
        })

        share = Share.objects.order_by('-id')[0]

        response = self.client.get(share.get_absolute_url())
        self.assertEqual(200, response.status_code)
        response_soup = BeautifulSoup(response.content)
        self.assertIsNotNone(response_soup.find('a', href=reverse("register")))

    def test_line_breaks_in_custom_message_show_as_paragraphs(self):
        self.assertEqual(len(mail.outbox), 0)

        url = reverse('share_assets_action')
        self.client.post(url, data={
            'asset_ids': self.asset.id,
            'recipient': 'test@example.com',
            'message': 'line one\n\nline two',
        })

        self.assertEqual(len(mail.outbox), 1)
        # Newlines should be converted to <p></p> in HTML version of email.
        email = mail.outbox[0]
        html_content = get_html_content(email)
        self.assertIn('<p>line one</p>', html_content)
        self.assertIn('<p>line two</p>', html_content)
        # Newlines should be left as is in plain text
        # version of email.
        plain_content = email.body
        self.assertIn('line one\n\nline two', plain_content)

        # Newlines should be converted to <p></p> in web page.
        share = Share.objects.order_by('-id')[0]
        response = self.client.get(share.get_absolute_url())
        self.assertContains(response, '<p>line one</p>')
        self.assertContains(response, '<p>line two</p>')

    def test_share_multiple_assets(self):
        asset2 = self.create_asset()

        url = reverse('share_assets_action')
        self.client.post(url, data={
            'asset_ids': ','.join([str(self.asset.id), str(asset2.id)]),
            'recipient': 'test@example.com',
        })

        # Make sure the shares have been saved to the database
        share = Share.objects.get()
        shared_asset_ids = {shared_asset.asset_id
                            for shared_asset in share.shared_assets.all()}
        expected_shared_asset_ids = {self.asset.id, asset2.id}
        self.assertEqual(expected_shared_asset_ids, shared_asset_ids)

        # Check email was sent
        self.assertEqual(len(mail.outbox), 1)
        email = mail.outbox[0]

        self.assertEqual(['test@example.com'], email.to)
        # Check that Assets (plural) not Asset (singular) is used
        self.assertNotIn('asset ', email.subject.lower())
        self.assertIn('assets', email.subject.lower())
        self.assertNotIn('asset ', email.body.lower())
        self.assertIn('assets', email.body.lower())

        # Now check that the share page shows download links for all the assets
        response = self.client.get(reverse('share', kwargs={
            'share_id': share.id,
            'key': share.key,
        }))
        self.assertEqual(200, response.status_code)
        response_soup = BeautifulSoup(response.content)
        for asset_id in expected_shared_asset_ids:
            link_element = response_soup.find(id='download_asset_%d' % asset_id)
            href = link_element['href']
            expected_href = reverse("shared_asset_download_action", kwargs={
                "share_id": share.id,
                "key": share.key,
                "asset_id": asset_id
            })
            self.assertEqual(expected_href, href)

    def test_sharing_creates_link(self):
        share = create_share_for_asset(self.asset)
        response = self.get_share_response(share)
        self.assertContains(response, escape(self.asset.filename))

    def test_invalid_share_id_403s(self):
        other_share = create_share_for_asset(self.asset)
        share = create_share_for_asset(self.asset)
        response = self.client.get(reverse('share',
                                           kwargs=dict(share_id=other_share.id,
                                                       key=share.key)))
        self.assertEqual(response.status_code, 403)

    def test_invalid_asset_id_403s(self):
        other_asset = self.create_asset()
        share = create_share_for_asset(self.asset)
        response = self.client.get(reverse('shared_asset_download_action',
                                           kwargs=dict(share_id=share.id,
                                                       key=share.key,
                                                       asset_id=other_asset.id)))
        self.assertEqual(response.status_code, 403)

    def test_invalid_key_403s(self):
        share = create_share_for_asset(self.asset)
        response = self.client.get(reverse('share',
                                           kwargs=dict(share_id=share.id,
                                                       key=share.key + 'test')))
        self.assertEqual(response.status_code, 403)

    def test_deleted_asset_explanation_page_shown(self):
        share = create_share_for_asset(self.asset)

        response = self.get_share_response(share)
        self.assertNotIn('has since been deleted', response.content)

        self.asset.delete()

        response = self.get_share_response(share)
        self.assertIn('has since been deleted', response.content)

    def test_expired_asset_explanation_page_shown(self):
        earlier = datetime.datetime.now() - datetime.timedelta(minutes=1)
        share = create_share_for_asset(self.asset, expiry=earlier)
        response = self.get_share_response(share)

        self.assertTemplateUsed(response, 'assetcloud/pages/logged_out/shared_asset_expired.html')
        self.assertEqual(earlier, response.context['share'].expiry)

    def test_expiry_set_when_assets_shared(self):
        url = reverse('share_assets_action')
        self.client.post(url, data={
            'asset_ids': self.asset.id,
            'recipient': 'test@example.com',
        })

        share = Share.objects.get()
        self.assertIsNotNone(share.expiry)
        # Check expiry is 30 days +/- 1 hour
        expected_expiry = datetime.datetime.now() + datetime.timedelta(days=30)
        self.assertLess(abs(expected_expiry - share.expiry), datetime.timedelta(hours=1))

    def get_share_response(self, share):
        response = self.client.get(reverse('share',
                                           kwargs=dict(share_id=share.id,
                                                       key=share.key)))
        self.assertEqual(response.status_code, 200)
        return response


class ShareAssetsActionViewTests(LoggedInTestCase):
    def test_asset_name_still_shown_after_validation_failure(self):
        asset = self.create_asset(title='Teh Titel')

        # Submit an invalid form (no recipient email)
        response = self.client.post(reverse('share_assets_action'), {
            'asset_ids': str(asset.id),
        })

        self.assertContains(response, asset.title)


class SharingValidityTests(LoggedInTestCase):
    def test_check_status_returns_asset_and_share_when_key_valid(self):
        asset = self.create_asset()
        share = share_asset(self.user, asset, 'test@example.com')
        status = sharing.check_asset_share_status(share.id, share.key, asset.id)
        (valid_asset, valid_share) = (status.asset, status.share)
        self.assertEqual(asset, valid_asset)
        self.assertEqual(share, valid_share)

    def test_check_status_returns_asset_not_found_when_asset_id_does_not_exist(self):
        asset = self.create_asset()
        asset_id = asset.id
        share = share_asset(self.user, asset, 'test@example.com')
        asset.delete()
        status = sharing.check_asset_share_status(share.id, share.key, asset_id)
        self.assertFalse(status.valid)
        self.assertEqual(sharing.SharingStatus.STATUS_ASSET_NOT_FOUND, status.status)
        if hasattr('status', 'asset'):
            self.assertIsNone(status.asset)

    def test_check_status_raises_permission_denied_when_key_is_incorrect(self):
        asset = self.create_asset()
        share = share_asset(self.user, asset, 'test@example.com')
        incorrect_key = 'BAD'
        with self.assertRaises(PermissionDenied):
            sharing.check_asset_share_status(share.id, incorrect_key, asset.id)

    def test_check_status_raises_permission_denied_when_asset_id_is_incorrect(self):
        shared_asset = self.create_asset()
        not_shared_asset = self.create_asset()
        share = share_asset(self.user, shared_asset, 'test@example.com')
        with self.assertRaises(PermissionDenied):
            sharing.check_asset_share_status(share.id, share.key, not_shared_asset.id)

    def test_check_status_returns_asset_and_share_when_key_valid_with_expiry(self):
        asset = self.create_asset()
        later = datetime.datetime.now() + datetime.timedelta(days=1)
        share = share_asset(self.user, asset, 'test@example.com', expiry=later)
        status = sharing.check_asset_share_status(share.id, share.key, asset.id)
        (valid_asset, valid_share) = (status.asset, status.share)
        self.assertEqual(asset, valid_asset)
        self.assertEqual(share, valid_share)

    def test_check_status_returns_expired_when_expired(self):
        asset = self.create_asset()
        earlier = datetime.datetime.now() - datetime.timedelta(minutes=1)
        share = share_asset(self.user, asset, 'test@example.com', expiry=earlier)
        status = sharing.check_asset_share_status(share.id, share.key, asset.id)
        self.assertFalse(status.valid)
        self.assertEqual(sharing.SharingStatus.STATUS_EXPIRED, status.status)
        if hasattr('status', 'asset'):
            self.assertIsNone(status.asset)
