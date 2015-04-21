# -*- coding: utf-8 -*-
from django.db import models

from django.db import models
from . import widgets


class GoogleMap(models.Model):
    name = models.CharField(max_length=255, verbose_name= 'Имя')
    map = widgets.LocationField(blank=True, verbose_name='Карта')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = u'Google Maps'
        verbose_name = u'Google Map'