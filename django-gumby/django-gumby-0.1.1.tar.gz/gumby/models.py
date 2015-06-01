# -*- coding: utf-8 -*-

from django.db import models


class HealthCheckModel(models.Model):
    title = models.CharField(max_length=128)
