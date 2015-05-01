# -*- coding: utf-8 -*-

from django.db import models
from django.utils.translation import ugettext_lazy as _


class TimeStampedModel(models.Model):
    """
    An abstract base class model that provides selfupdating "created" and
    "modified" fields.
    """
    created = models.DateTimeField(_('Created'), auto_now_add=True)
    modified = models.DateTimeField(_('Modified'), auto_now=True)

    class Meta:
        abstract = True


class StatusModel(models.Model):
    """
    An abstract base class model that provides a "status" field.
    """
    status = models.BooleanField(_(u'Status'), default=True)

    class Meta:
        abstract = True
