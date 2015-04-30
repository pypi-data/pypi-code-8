from django.db import models
from django.contrib.admin import site
import binascii
import os
from django.core import validators
from django.conf import settings
from django.contrib.auth.models import User
import uuid

AUTH_USER_MODEL = getattr(settings, 'AUTH_USER_MODEL', 'auth.User')

class Site(models.Model):
    uuid = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    title = models.CharField(verbose_name='站点名称',max_length=32)
    name = models.CharField(verbose_name='系统名称',validators=[
            validators.RegexValidator(r'^[a-z1-9]+$',
                                      ('系统名称只能为小写字母或者数字'), 'invalid'),
        ],max_length=32)

    def __str__(self):
        return self.title





class Signature(models.Model):
    site = models.ForeignKey(Site,related_name='signature')
    created = models.DateTimeField(auto_now_add=True)
    key = models.CharField(max_length=40)
    owner = models.ForeignKey(AUTH_USER_MODEL, related_name='signature', null=True,blank=True)

    def save(self, *args, **kwargs):
        if not self.key:
            self.key = self.generate_key()
        return super(Signature, self).save(*args, **kwargs)

    def generate_key(self):
        return binascii.hexlify(os.urandom(20)).decode()

    def __str__(self):
        return self.key



site.register( (Signature,Site,))