from django.test import TestCase as BaseTestCase
from django.test.client import Client as BaseClient, RequestFactory
from django.contrib.auth.models import User

from jmbo.models import Relation

from video.models import Video


class TestCase(BaseTestCase):

    @classmethod
    def setUpClass(cls):
        cls.request = RequestFactory()
        cls.client = BaseClient()

        # Editor
        cls.editor, dc = User.objects.get_or_create(
            username='editor',
            email='editor@test.com',
            is_superuser=True,
            is_staff=True,
        )
        cls.editor.set_password("password")
        cls.editor.save()

        # Video
        obj, dc = Video.objects.get_or_create(
            title='Video',
            content='Some content',
            stream='http://some.where.com/play.m3u8',
            owner=cls.editor, state='published',
        )
        obj.sites = [1]
        obj.save()
        cls.video = obj

    def test_admin_add(self):
        self.client.login(username="editor", password="password")
        response = self.client.get("/admin/video/video/add/")
        self.assertEquals(response.status_code, 200)

    def test_admin_change(self):
        self.client.login(username="editor", password="password")
        response = self.client.get("/admin/video/video/1/")
        self.assertEquals(response.status_code, 200)

    def test_detail(self):
        response = self.client.get("/video/video/")
        self.assertEquals(response.status_code, 200)
