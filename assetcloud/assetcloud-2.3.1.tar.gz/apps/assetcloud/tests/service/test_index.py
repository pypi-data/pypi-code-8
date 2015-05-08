# -*- coding: utf-8 -*-
# (c) 2012 Bright Interactive Limited. All rights reserved.
# http://www.bright-interactive.com | info@bright-interactive.com

from assetcloud.models import Asset
from assetcloud.tests.service.test_tagging import post_add_tags, post_delete_tags
from assetcloud.tests.service.utils import LoggedInTestCase


class AsyncIndexTests(LoggedInTestCase):
    needs_index = True

    # The async index relies on the asset's modified field, so we have a few
    # methods to test the modified field here.
    def test_modified_set_when_asset_created(self):
        asset = self.create_asset()
        self.assertIsNotNone(asset.modified)

    def test_modified_updated_when_asset_saved(self):
        asset = self.create_asset()
        old_modified = asset.modified

        asset.title = 'Changed'
        asset.save()

        self.assertGreater(asset.modified, old_modified)

    def test_modified_updated_when_asset_tags_added(self):
        asset = self.create_asset()
        old_modified = asset.modified

        response = post_add_tags(self.client, {'new'}, [asset])
        self.assertEqual(200, response.status_code)

        asset = Asset.unrestricted_objects.get(id=asset.id)

        self.assertGreater(asset.modified, old_modified)

    def test_modified_updated_when_asset_tags_deleted(self):
        asset = self.create_asset()

        response = post_add_tags(self.client, {'new'}, [asset])
        self.assertEqual(200, response.status_code)

        asset = Asset.unrestricted_objects.get(id=asset.id)
        old_modified = asset.modified

        response = post_delete_tags(self.client, {'new'}, [asset])
        self.assertEqual(200, response.status_code)

        asset = Asset.unrestricted_objects.get(id=asset.id)

        self.assertGreater(asset.modified, old_modified)
