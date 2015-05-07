# -*- coding: utf-8 -*-
# (c) 2011 Bright Interactive Limited. All rights reserved.
# http://www.bright-interactive.com | info@bright-interactive.com

"""
Service tests for REST API calls to do with Assets (/api/asset/*).
"""
from django.core.urlresolvers import reverse

from assetcloud.models import Asset
from assetcloud.tests.service.utils import create_asset, LoggedInTestCase, RoleTest


class AssetTitleAPITests(LoggedInTestCase):

    class RoleTestUpdateTitle(RoleTest):
        can = ['editor', 'admin']

        def when(self, test):
            old_title = "old title"
            self.new_title = "I'm a new title&&++=="
            self.asset = create_asset(user=test.user, title=old_title)
            test.assertEqual(old_title, self.asset.title)
            # we don't use reverse() here because one of the things that we want to
            # test is the actual concrete URL
            return test.client.post(reverse("asset-title-action", kwargs={"id": self.asset.id}),
                                    {'title': self.new_title})

        def role_can(self, test, response):
            test.assertEqual(200, response.status_code)

            # Reload asset
            asset = Asset.objects(test.user).get(id=self.asset.id)
            test.assertEqual(self.new_title, asset.title)

    def test_update_title_description_not_changed(self):
        old_title = "old title"
        new_title = "I'm a new title&&++=="

        description = 'asdfasfasdfa'

        asset = create_asset(user=self.user, title=old_title,
                             description=description)
        self.assertEqual(old_title, asset.title)
        self.assertEqual(description, asset.description)

        # we don't use reverse() here because one of the things that we want to
        # test is the actual concrete URL
        response = self.client.post(reverse('asset-title-action', kwargs={"id": asset.id}),
                {'title': new_title})
        self.assertEqual(200, response.status_code)

        # Reload asset
        asset = Asset.objects(self.user).get(id=asset.id)
        self.assertEqual(description, asset.description)
