# -*- coding: utf-8 -*-
from django.db import models
from . import widgets

from solo.models import SingletonModel
from filebrowser.fields import FileBrowseField

CHOICES_TYPE_OF_MAP = (('YM', 'Яндекс Карта',), ('GM', 'Google Карта',))
CHOICES_TYPE_OF_DISPLAY = (('ROADMAP', 'Карта',), ('HYBRID', 'Спутник',))

class Map(SingletonModel):
    name = models.CharField(blank=False, null=False, max_length=255, verbose_name='Заголовок')
    map = widgets.LocationField(blank=False, null=False, verbose_name='Карта')
    zoom = models.IntegerField(blank=False, null=False, default='14', verbose_name='Зум')
    mapDisplayType = models.CharField(max_length=7, choices=CHOICES_TYPE_OF_DISPLAY, default='ROADMAP', verbose_name='Тип Отображения карты')
    baloon = models.TextField(blank=True, verbose_name='Текст балуна')
    markerImg = FileBrowseField(max_length=300, directory="'marker", extensions=[".jpg", ".png", ".jpeg", ".ico", ], blank=False, null=False, verbose_name='Картинка для метки')
    mapType = models.CharField(max_length=2, choices=CHOICES_TYPE_OF_MAP, default='YM', verbose_name='Тип карты')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = u'Карты'
        verbose_name = u'Карта'