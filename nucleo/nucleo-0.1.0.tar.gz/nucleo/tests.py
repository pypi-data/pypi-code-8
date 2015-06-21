try:
    import json
except ImportError:
    import simplejson as json
from django.test import TestCase
from django.contrib.auth.models import User


class TestNucleoApi(TestCase):
    '''API TESTs'''

    fixtures = ['user.json', 'post.json', 'userprofile.json']

    def setUp(self):
        self.mock_user = {
            'email': 'g0ph@g0ph.com',
            'name': 'g0ph',
            'password': 'g0ph',
        }
        # User.objects.create_user(self.mock_user['name'],
        #                          self.mock_user['email'],
        #                          self.mock_user['password'])
        self.client.login(
            username=self.mock_user['name'],
            password=self.mock_user['password'],
        )
        # Each self.client.get show pass follow=True

    def test_following(self):
        # test a normal "logged-in" situation
        response = self.client.post('/api/following', {})
        self.assertEqual(response.status_code, 200)
        following = json.loads(response.content)
        assert 'user1' in following
        # Log out and check what comes out
        self.client.logout()
        response = self.client.post('/api/following', {})
        self.assertEqual(response.status_code, 200)
        following = json.loads(response.content)
        assert len(following) == 0

