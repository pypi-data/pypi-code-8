# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import ecl_tools.bulkmail.models


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Campaign',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('subject', models.CharField(max_length=255)),
                ('html', models.TextField()),
                ('text', models.TextField()),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('sent', models.DateTimeField(null=True, blank=True)),
                ('scheduled', models.DateTimeField(null=True, blank=True)),
            ],
            options={
                'ordering': ('-created',),
            },
        ),
        migrations.CreateModel(
            name='List',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=70)),
                ('from_name', models.CharField(max_length=70)),
                ('reply_to', models.EmailField(max_length=254, verbose_name=b'Reply to Address')),
                ('mail_domain', models.CharField(max_length=70)),
                ('address', models.TextField(help_text=b'Include physical address and phone number for complaints.')),
                ('short_description', models.CharField(max_length=70)),
                ('frequency', models.CharField(max_length=70)),
                ('description', models.TextField()),
                ('sorder', models.IntegerField(verbose_name=b'Order')),
            ],
            options={
                'ordering': ('sorder',),
            },
        ),
        migrations.CreateModel(
            name='Optin',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('email', models.EmailField(max_length=254)),
                ('skey', models.CharField(max_length=255)),
                ('signup_location', models.CharField(max_length=300, null=True, blank=True)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('bulk_lists', models.ManyToManyField(to='bulkmail.List')),
            ],
            bases=(ecl_tools.bulkmail.models.BaseBulkmail, models.Model),
        ),
        migrations.CreateModel(
            name='Subscription',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('email', models.EmailField(max_length=254)),
                ('email_status', models.CharField(default=b'no-process', max_length=255, null=True, blank=True, choices=[(b'clean', b'Clean'), (b'trap', b'Spam Trap'), (b'invalid', b'Invalid'), (b'bounce', b'Bounce'), (b'suspicious', b'Suspicious'), (b'processing', b'Processing'), (b'no-process', b'Not Processed')])),
                ('is_clean', models.BooleanField(default=False)),
                ('signup_location', models.CharField(max_length=300, null=True, blank=True)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('bounce1', models.DateTimeField(null=True, blank=True)),
                ('bounce2', models.DateTimeField(null=True, blank=True)),
                ('complaint', models.DateTimeField(null=True, blank=True)),
                ('unsubscribed', models.DateTimeField(null=True, blank=True)),
                ('reason', models.CharField(blank=True, max_length=255, null=True, choices=[(b'bounce', b'Bounced'), (b'complaint', b'Complaint'), (b'dead-address', b'Dead Address'), (b'no-opens', b'No Activity'), (b'bad-email', b'Bad Email')])),
                ('bulk_list', models.ForeignKey(to='bulkmail.List')),
            ],
        ),
        migrations.CreateModel(
            name='TrackingEvent',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('campaign', models.CharField(max_length=50)),
                ('event', models.CharField(max_length=12, choices=[(b'opened', b'opened'), (b'clicked', b'clicked'), (b'unsubscribed', b'unsubscribed'), (b'complained', b'complained'), (b'bounced', b'bounced'), (b'dropped', b'dropped'), (b'delivered', b'delivered')])),
                ('client_os', models.CharField(max_length=50, null=True, blank=True)),
                ('client_name', models.CharField(max_length=50, null=True, blank=True)),
                ('client_type', models.CharField(max_length=50, null=True, blank=True)),
                ('device_type', models.CharField(max_length=50, null=True, blank=True)),
                ('user_agent', models.CharField(max_length=1000, null=True, blank=True)),
                ('city', models.CharField(max_length=50, null=True, blank=True)),
                ('region', models.CharField(max_length=10, null=True, blank=True)),
                ('country', models.CharField(max_length=10, null=True, blank=True)),
                ('ip', models.CharField(max_length=15, null=True, blank=True)),
                ('time', models.DateTimeField(null=True, blank=True)),
                ('subscription', models.ForeignKey(to='bulkmail.Subscription')),
            ],
        ),
        migrations.AddField(
            model_name='campaign',
            name='bulk_list',
            field=models.ForeignKey(to='bulkmail.List'),
        ),
    ]
