# -*-coding: utf-8 -*-
from django.db import models


class DBLogEntry(models.Model):
    time = models.DateTimeField(auto_now_add=True)
    level = models.CharField(max_length=10)
    message = models.TextField()

    def __str__(self):
        return str(self.time.strftime("%d.%B.%Y %H:%M"))+" "+str(self.level)
