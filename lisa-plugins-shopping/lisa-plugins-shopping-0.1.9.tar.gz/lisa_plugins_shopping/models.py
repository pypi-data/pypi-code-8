from django.db import models
from jsonfield import JSONField


class ShoppingList(models.Model):
    name = models.CharField(max_length=100, unique=True)
    list = JSONField()

    def save(self, force_insert=False, force_update=False, using=None,
             update_fields=None):
        self.name = self.name.lower()
        super(ShoppingList, self).save(force_insert, force_update)
