from django.db import models

from assetcloud.asset_metadata_util import BaseMetadataModel
from assetcloud.models import Asset


class TestAssetMetadataModel(models.Model):
    asset = models.OneToOneField(Asset, related_name="metadata", primary_key=True)
    required_field = models.CharField(max_length=100)
    non_required_field = models.CharField(max_length=100, blank=True)


class AnotherTestAssetMetadataModel(models.Model):
    asset = models.OneToOneField(Asset, related_name="more_metadata", primary_key=True)
    another_required_field = models.CharField(max_length=100)
    another_non_required_field = models.CharField(max_length=100, blank=True)


class TestModel(models.Model):
    def __unicode__(self):
        return self.name

    name = models.CharField(max_length=120)


class MetadataModelWithManyToMany(models.Model):
    asset = models.OneToOneField(Asset, related_name="m2m_metadata")
    tests = models.ManyToManyField(TestModel, null=True, blank=True)


class CreateOnSaveMetadataModel(BaseMetadataModel):
    asset = models.OneToOneField(Asset, related_name="create_on_save_metadata")
    non_required_field = models.CharField(max_length=100, blank=True)

    class MetadataMeta:
        create_on_save = True
