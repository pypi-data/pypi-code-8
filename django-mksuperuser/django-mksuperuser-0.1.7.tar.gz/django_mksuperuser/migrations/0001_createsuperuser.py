# -*- coding: utf-8 -*-
from __future__ import unicode_literals

try:
    from django.db.migrations import Migration, RunPython
except ImportError:
    # are you using South?
    # south is also using migrations dir
    class Migration(object):
        def forwards(self, orm):
            pass

    RunPython = lambda x: x
from django.contrib.auth.admin import User


def create_superuser(apps, schema_editor):
    superuser = User()
    superuser.is_active = True
    superuser.is_superuser = True
    superuser.is_staff = True
    superuser.username = 'admin'
    superuser.email = 'admin@admin.net'
    superuser.set_password('admin')
    superuser.save()


class Migration(Migration):

    dependencies = [
    ]

    operations = [
        RunPython(create_superuser)
    ]
