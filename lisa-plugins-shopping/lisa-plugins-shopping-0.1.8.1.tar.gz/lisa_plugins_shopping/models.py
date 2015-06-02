from django.db import models
from jsonfield import JSONField


class ShoppingList(models.Model):
    name = models.CharField(max_length=100, unique=True)
    list = JSONField()