from django.db import models

from ..model.models import BaseListModel, BaseUuidModel


class TestModel(BaseUuidModel):

    f1 = models.CharField(max_length=10)
    f2 = models.CharField(max_length=10)
    f3 = models.CharField(max_length=10, null=True, blank=False)
    f4 = models.CharField(max_length=10, null=True, blank=False)
    f5 = models.CharField(max_length=10)

    class Meta:
        app_label = 'edc_base'


class TestM2m(BaseListModel):

    class Meta:
        app_label = 'edc_base'


class TestForeignKey(BaseListModel):

    class Meta:
        app_label = 'edc_base'
