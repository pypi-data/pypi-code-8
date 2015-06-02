from django.db import models


class Configuration(models.Model):
    address = models.CharField(max_length=100, unique=True)
    port = models.CharField(max_length=5)
    room = models.CharField(max_length=50)