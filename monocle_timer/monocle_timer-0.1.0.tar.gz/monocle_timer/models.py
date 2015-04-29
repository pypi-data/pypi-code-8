# -*- coding: utf-8 -*-
from django.db import models
from solo.models import SingletonModel

import datetime
from django.utils.timezone import utc

class Timer(SingletonModel):
    text = models.TextField(verbose_name=u'Текст акции', help_text=u'Не более 200 символов', blank=False)
    deadline = models.DateTimeField(verbose_name=u'Срок окончания акции', blank=False)
    isShown = models.BooleanField(default=True,help_text= u'Отображать таймер на сайте', verbose_name=u'Показывать')

    def get_countdown(self):
        #get current time
        now = datetime.datetime.utcnow().replace(tzinfo=utc)

        #calculate time difference
        self.delta = (self.deadline - now)

        #return rounded seconds
        return int(self.delta.total_seconds())

    def __str__(self):
        return u'Таймер'

    class Meta:
        verbose_name_plural = u'Таймер'
        verbose_name = u'Таймер'