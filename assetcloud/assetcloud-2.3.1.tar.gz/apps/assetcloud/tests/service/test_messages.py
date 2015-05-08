from django.core.urlresolvers import reverse
from .utils import AdminLoggedInTestCase, create_fake_request
from django.contrib import messages
from assetcloud.views import messages_action


class MessageTests(AdminLoggedInTestCase):
    def test_message_div_always_available(self):
        self.assertIn('class="messages',
                      self.client.get(reverse('asset-upload'), follow=True).content)

    def get_messages(self, request):
        return messages_action(request)

    def test_messages_action_returns_messages(self):
        request = create_fake_request(self.user)
        messages.info(request, 'Test message 1')
        messages.info(request, 'Test message 2')
        response = self.get_messages(request)
        self.assertIn('Test message 1', response.content)
        self.assertIn('Test message 2', response.content)

    def test_messages_action_empty_when_no_messages(self):
        request = create_fake_request(self.user)
        response = self.get_messages(request)
        self.assertEqual('', response.content)
