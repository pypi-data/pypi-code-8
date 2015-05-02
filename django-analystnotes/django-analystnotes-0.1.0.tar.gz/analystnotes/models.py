# -*- coding: utf-8 -*-
from django.db import models
from django.contrib.auth.models import User


class Project(models.Model):
    """  A Project that is assigned to a user
    """
    name = models.CharField('Name of project', max_length=64, db_index=True, unique=False)
    slug = models.SlugField('Slug Name', max_length=128, db_index=True, unique=True)
    created = models.DateTimeField('Date project created', db_index=True, unique=False, auto_now_add=True)
    owner = models.ForeignKey(User)

    def __unicode__(self):
        return '%s' % self.name


class Command(models.Model):
    """ Command output """
    project = models.ForeignKey(Project)
    cmd = models.CharField('Command', max_length=2048, db_index=True, unique=False)
    stdout = models.TextField('Standard Out', blank=True, null=True)
    stderr = models.TextField('Standard Error', blank=True, null=True)
    execute_time = models.DateTimeField('Process Execute Time', auto_now_add=True)
    exitcode = models.IntegerField('Process Exit Code', db_index=True, blank=False)
