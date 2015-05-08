# (c) 2011 Bright Interactive Limited. All rights reserved.
# http://www.bright-interactive.com | info@bright-interactive.com

"""
Haystack search index configuration for the Asset Cloud app.
"""
from haystack.indexes import SearchIndex

from assetcloud.models import Asset
from django.db import models
from haystack import indexes, connections, signals
import datetime


class AssetQueuedSignalProcessor(signals.BaseSignalProcessor):
    """
    Co-operates with UpdateIndexMiddleware to processes additions to the index
    in bulk at the end of the request.

    Processes deletes synchronously because that was easier to implement than
    queueing them and we weren't suffering performance problems with deletes.
    We could change it in future so that deletes are queued as well.
    """

    def setup(self):
        models.signals.post_save.connect(AssetIndex.update_index_maybe_later, sender=Asset)
        models.signals.post_delete.connect(self.handle_delete, sender=Asset)

    def teardown(self):
        models.signals.post_save.disconnect(AssetIndex.update_index_maybe_later, sender=Asset)
        models.signals.post_delete.disconnect(self.handle_delete, sender=Asset)


class AssetIndex(SearchIndex, indexes.Indexable):
    text = indexes.CharField(document=True, use_template=True)
    # This field is called account instead of account_id to make it so that
    # AssetQuerySet.filter_for_user() can be written to work on both
    # SearchQuerySets and database QuerySets.
    account = indexes.IntegerField(model_attr='account_id', null=True)
    # Called upload instead of upload_id just to be consistent with account.
    upload = indexes.IntegerField(model_attr='upload_id')
    added = indexes.DateField(model_attr='added')
    tags = indexes.MultiValueField()
    folders = indexes.MultiValueField()

    def prepare_tags(self, obj):
        return [tag.id for tag in obj.tags.all()]

    def prepare_folders(self, obj):
        return [folder.id for folder in obj.folders.all()]

    def get_model(self):
        return Asset

    def update_objects(self, instances):
        connections['default'].get_backend().update(self, instances)

    @classmethod
    def update_index_maybe_later(cls, *args, **kwargs):
        from assetcloud.index import update_index_maybe_later
        update_index_maybe_later()


def reindex_asset_maybe_later(asset):
    """
    Reindex an asset at some point in the future.
    """
    if asset is not None:
        # Update the asset's modified date so that
        # assetcloud.index.get_assets_to_index() will include it
        asset.modified = datetime.datetime.now()
        asset.save()
        connections['default'].get_unified_index().get_index(Asset).update_index_maybe_later()
