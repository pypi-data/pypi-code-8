# -*- coding: utf-8 -*-
from django.db import models

CHOICES_PAGIN = (('true', 'С пагинацией',), ('false', 'Без пагинации',))
CHOICES_ARROWS = (('true', 'Со стрелками',), ('false', 'Без стрелок',))

from filebrowser.fields import FileBrowseField

class Slider(models.Model):
    name = models.CharField(max_length=255, verbose_name= 'Название слайдера')
    text = models.TextField(verbose_name='Подпись')
    elem_number = models.PositiveSmallIntegerField(blank=False, default=1, verbose_name='Количество отображаемых слайдов')
    isShown = models.BooleanField(default=True, verbose_name= 'Показывать')
    arrows = models.CharField(max_length=5, choices=CHOICES_ARROWS, default='true', blank=False, verbose_name='Стрелки навигации')
    pagination = models.CharField(max_length=5, choices=CHOICES_PAGIN, default='true', blank=False, verbose_name='Пагинация')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = u'Слайдеры'
        verbose_name = u'Слайдер'

class Slide(models.Model):
    name = models.CharField(max_length=255, verbose_name='Название')
    slider = models.ForeignKey('Slider', verbose_name= 'Слайдер')
    image = FileBrowseField(max_length=200, directory="'slider", extensions=[".jpg", ".png", ".jpeg", ".ico", ], blank=True, null=True, verbose_name= 'Изображение')
    text = models.TextField(verbose_name='Подпись', blank=True)
    isShown = models.BooleanField(default=True, verbose_name='Показывать слайд')
    position = models.PositiveSmallIntegerField(default=0)

    class Meta:
        verbose_name_plural = u'Слайды'
        verbose_name = u'Слайд'
        ordering = ['position']