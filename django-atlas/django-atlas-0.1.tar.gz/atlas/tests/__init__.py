from django.test import TestCase as BaseTestCase
from django.test.client import Client, RequestFactory
from django.contrib.auth.models import User


class TestCase(BaseTestCase):

    @classmethod
    def setUpClass(cls):
        cls.request = RequestFactory()
        cls.client = Client()

        # Editor
        cls.editor, dc = User.objects.get_or_create(
            username='editor',
            email='editor@test.com',
            is_superuser=True,
            is_staff=True,
        )
        cls.editor.set_password("password")
        cls.editor.save()

    def test_something(self):
        self.fail("No tests exist yet!")
