# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import datetime
from dateutil.relativedelta import relativedelta
from stdimage.models import StdImageField
from stdimage.validators import MinSizeValidator

from django.db import models
from django.utils.translation import ugettext as _
from . import app_settings


class Sponsor(models.Model):
    """
    Model for ...
    """
    SPONSOR_TYPES = (
        (0, _('NONE')),
        (1, _('PLATINUM')),
        (2, _('GOLD')),
        (3, _('SILVER')),
        (4, _('BRONCE')),
    )
    SPONSOR_TYPES_REV = dict((y, x) for x, y in SPONSOR_TYPES)

    enabled = models.BooleanField(default=True, null=False)
    name = models.CharField(null=False, blank=False, max_length=30)
    description = models.TextField(blank=True, null=True, default=None)
    logo = models.ImageField(upload_to='logos/', null=True, blank=True)
    # logo = StdImageField(upload_to='logos/',
    #                      null=True, blank=True,
    #                      variations={'thumbnail': {'with': 200, 'height': 175}},
    #                      validators=MinSizeValidator(150, 100))

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    expires_on = models.DateTimeField(default=datetime.datetime.now()+relativedelta(months=+app_settings.SPONSOR_EXPIRE_ON_MONTHS))
    does_expire = models.BooleanField(default=app_settings.SPONSOR_EXPIRATES, null=False, blank=True)
    type = models.PositiveIntegerField(choices=SPONSOR_TYPES, default=0, null=False, blank=True)
    width = models.PositiveIntegerField(default=app_settings.SPONSOR_LOGO_WIDTH, null=False, blank=True)
    height = models.PositiveIntegerField(default=app_settings.SPONSOR_LOGO_HEIGHT, null=True, blank=True)

    def __unicode__(self):
        return '{} - {}'.format(self.name, self.type)

    @classmethod
    def get_all_sponsors(cls):
        return cls.objects.filter(enabled=True)

    @classmethod
    def get_expired_sponsors(cls):
        return cls.get_all_sponsors().filter(does_expire=True, expires_on__lt=datetime.datetime.now())

    @classmethod
    def get_disabled_sponsors(cls):
        return cls.objects.filter(enabled=False)


# TODO: Optionally logo size dependant on sponsor type
# TODO: Custom logo size and create thumbnail automatically
# TODO: Sponsor Join View
# TODO: Sponsor Forms: join
