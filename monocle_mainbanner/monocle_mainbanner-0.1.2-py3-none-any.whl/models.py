# -*- coding: utf-8 -*-
from django.db import models

CHOICES_PAGIN = (('true', 'С пагинацией',), ('false', 'Без пагинации',))
CHOICES_ARROWS = (('true', 'Со стелками',), ('false', 'Без стелок',))

from filebrowser.fields import FileBrowseField

class MainBanner(models.Model):
    name = models.CharField(max_length=255, verbose_name='Заголовок')
    text = models.TextField(verbose_name='Подпись')
    elem_number = models.PositiveSmallIntegerField(blank=False, default=1, verbose_name='Количество отображаемых слайдов')
    width = models.BooleanField(default=True, verbose_name='По ширине экрана')
    isShown = models.BooleanField(default=True, verbose_name='Показывать')
    arrows = models.CharField(max_length=5, choices=CHOICES_ARROWS, default='false', blank=False, verbose_name='Стрелки навигации')
    pagination = models.CharField(max_length=5, choices=CHOICES_PAGIN, default='false', blank=False, verbose_name='Пагинация')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = u'Главный баннер'
        verbose_name = u'Главный баннер'


class Slide(models.Model):
    name = models.CharField(max_length=255, verbose_name= 'Заголовок')
    slider = models.ForeignKey('MainBanner', verbose_name= 'Баннер')
    image = FileBrowseField(max_length=200, directory="'banner", extensions=[".jpg", ".png", ".jpeg"], blank=True, null=True, verbose_name= 'Изображение')
    text = models.TextField(verbose_name='Подпись', blank=True)
    isShown = models.BooleanField(default=True, verbose_name='Показывать')
    position = models.PositiveSmallIntegerField(default=0)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = u'Слайды'
        verbose_name = u'Слайд'
        ordering = ['position']