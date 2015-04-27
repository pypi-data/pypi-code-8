# -*- coding: utf-8 -*-
from django.db import models
from . import widgets

from solo.models import SingletonModel

CHOICES = (('YM', 'Яндекс Карта',), ('GM', 'Google Карта',))

class Map(SingletonModel):
    name = models.CharField(blank=False, null=False, max_length=255, verbose_name='Заголовок')
    map = widgets.LocationField(blank=False, null=False, verbose_name='Карта')
    zoom = models.IntegerField(blank=False, null=False, default='14', verbose_name='Зум')
    baloon = models.TextField(blank=True, verbose_name='Текст балуна')
    markerImg = models.ImageField(upload_to='marker', blank=False, verbose_name='Картинка для метки')
    mapType = models.CharField(max_length=2, choices=CHOICES, default='YM', verbose_name='Тип карты')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = u'Карты'
        verbose_name = u'Карта'