# -*- coding: utf-8 -*-
from django.db import models

CHOICES = (('send', 'Отправка писем',), ('text', 'Текстовое модальное окно',))

class Modal(models.Model):
    name = models.CharField(max_length=255, default= 'Заказать звонок', verbose_name='Заголовок', help_text='Ввидите заголовок всплывющего окна')
    modal_id = models.CharField(max_length=50, verbose_name='id Модального окна')
    text = models.TextField(blank=True, verbose_name='Текст')
    mandrill_api_key = models.CharField(max_length=255, blank=True, default= 'uwvfAAW-VFOYMAyj1kBrfA', verbose_name='API-ключ для Mandrill', help_text='Пример: uwvfAAW-VFOYMAyj1kBrfA')
    email = models.EmailField(blank=True, verbose_name='Email для отправки писем', help_text='Почтовый ящик на который будут приходить письма')
    type = models.CharField(max_length=5, choices=CHOICES, default='send', blank=False, verbose_name='Тип модального окна')

    showEmail = models.BooleanField(default=True, verbose_name='Отображать')
    requiredEmail = models.BooleanField(default=True, verbose_name='Обязателеное')
    showPhone = models.BooleanField(default=True, verbose_name='Отображать')
    requiredPhone = models.BooleanField(default=True, verbose_name='Обязателеное')
    showMessage = models.BooleanField(default=True, verbose_name='Отображать')
    requiredMessage = models.BooleanField(default=False, verbose_name='Обязателеное')

    buttonText = models.CharField(max_length=50, blank=True, default='Отправить', verbose_name='Текст для кнопки')

    resModal = models.BooleanField(default=False, verbose_name='Отображать окно при успещной отправке письма')
    resModalText = models.TextField(blank=True, verbose_name='Текст результирующего окна', help_text='Текст окна, которое отображается после успешной отправки письма')

    def underscored_id(self):
        return self.modal_id.replace(' ', '_').replace('-', '_').replace('#', '')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = u'Модальные окна'
        verbose_name = u'Модальное окно'

from django.apps import AppConfig
class CustomAppConfig(AppConfig):
    name = 'apps.monocle_modals'
    verbose_name = 'Модальные окна'