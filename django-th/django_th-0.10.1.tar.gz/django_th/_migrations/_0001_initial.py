# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
       migrations.CreateModel(
            name='ServicesActivated',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(unique=True, max_length=200)),
                ('status', models.BooleanField(default=False)),
                ('auth_required', models.BooleanField(default=True)),
                ('description', models.CharField(max_length=200)),
            ],
            options={
                'verbose_name': 'Services',
                'verbose_name_plural': 'Services',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='TriggerService',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('description', models.CharField(max_length=200)),
                ('date_created', models.DateField(auto_now_add=True)),
                ('date_triggered', models.DateTimeField(null=True)),
                ('status', models.BooleanField(default=False)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='UserProfile',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('user', models.OneToOneField(to=settings.AUTH_USER_MODEL)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='UserService',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('token', models.CharField(max_length=255)),
                ('name', models.ForeignKey(related_name='+', to='django_th.ServicesActivated', to_field=b'name')),
                ('user', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='triggerservice',
            name='consumer',
            field=models.ForeignKey(related_name='+', blank=True, to='django_th.UserService'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='triggerservice',
            name='provider',
            field=models.ForeignKey(related_name='+', blank=True, to='django_th.UserService'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='triggerservice',
            name='user',
            field=models.ForeignKey(to=settings.AUTH_USER_MODEL),
            preserve_default=True,
        ),
    ]
