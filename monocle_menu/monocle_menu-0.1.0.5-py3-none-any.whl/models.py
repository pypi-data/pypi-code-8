# -*- coding: utf-8 -*-
from django.db import models

class Menu(models.Model):
    name = models.CharField(max_length=255, verbose_name='Название пункта меню')
    anchor = models.CharField(max_length=255, verbose_name='ID блока')
    position = models.PositiveIntegerField(default=0)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = u'Меню'
        verbose_name = u'Элемент меню'
        ordering = ['position']


