from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

class SecureAdmin(models.Model):
    user = models.ForeignKey(User)
    ip = models.CharField(max_length=10000,blank=True)
    ipmail = models.CharField(max_length=100,blank=True)
    ipcode = models.CharField(max_length=100,blank=True)

