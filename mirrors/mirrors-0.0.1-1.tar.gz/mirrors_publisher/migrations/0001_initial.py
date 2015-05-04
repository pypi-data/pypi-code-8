# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('mirrors', '0014_auto_20150224_2252'),
    ]

    operations = [
        migrations.CreateModel(
            name='PublishReceipt',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('publish_datetime', models.DateTimeField(auto_now_add=True)),
                ('component', models.ForeignKey(to='mirrors.Component', related_name='publish_receipts')),
                ('revision', models.ForeignKey(to='mirrors.ComponentRevision', related_name='+')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
    ]
