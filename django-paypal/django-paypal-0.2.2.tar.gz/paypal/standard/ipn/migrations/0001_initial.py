# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='PayPalIPN',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('business', models.CharField(help_text='Email where the money was sent.', max_length=127, blank=True)),
                ('charset', models.CharField(max_length=32, blank=True)),
                ('custom', models.CharField(max_length=255, blank=True)),
                ('notify_version', models.DecimalField(default=0, null=True, max_digits=64, decimal_places=2, blank=True)),
                ('parent_txn_id', models.CharField(max_length=19, verbose_name='Parent Transaction ID', blank=True)),
                ('receiver_email', models.EmailField(max_length=127, blank=True)),
                ('receiver_id', models.CharField(max_length=127, blank=True)),
                ('residence_country', models.CharField(max_length=2, blank=True)),
                ('test_ipn', models.BooleanField(default=False)),
                ('txn_id', models.CharField(help_text='PayPal transaction ID.', max_length=19, verbose_name='Transaction ID', db_index=True, blank=True)),
                ('txn_type', models.CharField(help_text='PayPal transaction type.', max_length=128, verbose_name='Transaction Type', blank=True)),
                ('verify_sign', models.CharField(max_length=255, blank=True)),
                ('address_country', models.CharField(max_length=64, blank=True)),
                ('address_city', models.CharField(max_length=40, blank=True)),
                ('address_country_code', models.CharField(help_text='ISO 3166', max_length=64, blank=True)),
                ('address_name', models.CharField(max_length=128, blank=True)),
                ('address_state', models.CharField(max_length=40, blank=True)),
                ('address_status', models.CharField(max_length=11, blank=True)),
                ('address_street', models.CharField(max_length=200, blank=True)),
                ('address_zip', models.CharField(max_length=20, blank=True)),
                ('contact_phone', models.CharField(max_length=20, blank=True)),
                ('first_name', models.CharField(max_length=64, blank=True)),
                ('last_name', models.CharField(max_length=64, blank=True)),
                ('payer_business_name', models.CharField(max_length=127, blank=True)),
                ('payer_email', models.CharField(max_length=127, blank=True)),
                ('payer_id', models.CharField(max_length=13, blank=True)),
                ('auth_amount', models.DecimalField(default=0, null=True, max_digits=64, decimal_places=2, blank=True)),
                ('auth_exp', models.CharField(max_length=28, blank=True)),
                ('auth_id', models.CharField(max_length=19, blank=True)),
                ('auth_status', models.CharField(max_length=9, blank=True)),
                ('exchange_rate', models.DecimalField(default=0, null=True, max_digits=64, decimal_places=16, blank=True)),
                ('invoice', models.CharField(max_length=127, blank=True)),
                ('item_name', models.CharField(max_length=127, blank=True)),
                ('item_number', models.CharField(max_length=127, blank=True)),
                ('mc_currency', models.CharField(default='USD', max_length=32, blank=True)),
                ('mc_fee', models.DecimalField(default=0, null=True, max_digits=64, decimal_places=2, blank=True)),
                ('mc_gross', models.DecimalField(default=0, null=True, max_digits=64, decimal_places=2, blank=True)),
                ('mc_handling', models.DecimalField(default=0, null=True, max_digits=64, decimal_places=2, blank=True)),
                ('mc_shipping', models.DecimalField(default=0, null=True, max_digits=64, decimal_places=2, blank=True)),
                ('memo', models.CharField(max_length=255, blank=True)),
                ('num_cart_items', models.IntegerField(default=0, null=True, blank=True)),
                ('option_name1', models.CharField(max_length=64, blank=True)),
                ('option_name2', models.CharField(max_length=64, blank=True)),
                ('payer_status', models.CharField(max_length=10, blank=True)),
                ('payment_date', models.DateTimeField(help_text='HH:MM:SS DD Mmm YY, YYYY PST', null=True, blank=True)),
                ('payment_gross', models.DecimalField(default=0, null=True, max_digits=64, decimal_places=2, blank=True)),
                ('payment_status', models.CharField(max_length=17, blank=True)),
                ('payment_type', models.CharField(max_length=7, blank=True)),
                ('pending_reason', models.CharField(max_length=14, blank=True)),
                ('protection_eligibility', models.CharField(max_length=32, blank=True)),
                ('quantity', models.IntegerField(default=1, null=True, blank=True)),
                ('reason_code', models.CharField(max_length=15, blank=True)),
                ('remaining_settle', models.DecimalField(default=0, null=True, max_digits=64, decimal_places=2, blank=True)),
                ('settle_amount', models.DecimalField(default=0, null=True, max_digits=64, decimal_places=2, blank=True)),
                ('settle_currency', models.CharField(max_length=32, blank=True)),
                ('shipping', models.DecimalField(default=0, null=True, max_digits=64, decimal_places=2, blank=True)),
                ('shipping_method', models.CharField(max_length=255, blank=True)),
                ('tax', models.DecimalField(default=0, null=True, max_digits=64, decimal_places=2, blank=True)),
                ('transaction_entity', models.CharField(max_length=7, blank=True)),
                ('auction_buyer_id', models.CharField(max_length=64, blank=True)),
                ('auction_closing_date', models.DateTimeField(help_text='HH:MM:SS DD Mmm YY, YYYY PST', null=True, blank=True)),
                ('auction_multi_item', models.IntegerField(default=0, null=True, blank=True)),
                ('for_auction', models.DecimalField(default=0, null=True, max_digits=64, decimal_places=2, blank=True)),
                ('amount', models.DecimalField(default=0, null=True, max_digits=64, decimal_places=2, blank=True)),
                ('amount_per_cycle', models.DecimalField(default=0, null=True, max_digits=64, decimal_places=2, blank=True)),
                ('initial_payment_amount', models.DecimalField(default=0, null=True, max_digits=64, decimal_places=2, blank=True)),
                ('next_payment_date', models.DateTimeField(help_text='HH:MM:SS DD Mmm YY, YYYY PST', null=True, blank=True)),
                ('outstanding_balance', models.DecimalField(default=0, null=True, max_digits=64, decimal_places=2, blank=True)),
                ('payment_cycle', models.CharField(max_length=32, blank=True)),
                ('period_type', models.CharField(max_length=32, blank=True)),
                ('product_name', models.CharField(max_length=128, blank=True)),
                ('product_type', models.CharField(max_length=128, blank=True)),
                ('profile_status', models.CharField(max_length=32, blank=True)),
                ('recurring_payment_id', models.CharField(max_length=128, blank=True)),
                ('rp_invoice_id', models.CharField(max_length=127, blank=True)),
                ('time_created', models.DateTimeField(help_text='HH:MM:SS DD Mmm YY, YYYY PST', null=True, blank=True)),
                ('amount1', models.DecimalField(default=0, null=True, max_digits=64, decimal_places=2, blank=True)),
                ('amount2', models.DecimalField(default=0, null=True, max_digits=64, decimal_places=2, blank=True)),
                ('amount3', models.DecimalField(default=0, null=True, max_digits=64, decimal_places=2, blank=True)),
                ('mc_amount1', models.DecimalField(default=0, null=True, max_digits=64, decimal_places=2, blank=True)),
                ('mc_amount2', models.DecimalField(default=0, null=True, max_digits=64, decimal_places=2, blank=True)),
                ('mc_amount3', models.DecimalField(default=0, null=True, max_digits=64, decimal_places=2, blank=True)),
                ('password', models.CharField(max_length=24, blank=True)),
                ('period1', models.CharField(max_length=32, blank=True)),
                ('period2', models.CharField(max_length=32, blank=True)),
                ('period3', models.CharField(max_length=32, blank=True)),
                ('reattempt', models.CharField(max_length=1, blank=True)),
                ('recur_times', models.IntegerField(default=0, null=True, blank=True)),
                ('recurring', models.CharField(max_length=1, blank=True)),
                ('retry_at', models.DateTimeField(help_text='HH:MM:SS DD Mmm YY, YYYY PST', null=True, blank=True)),
                ('subscr_date', models.DateTimeField(help_text='HH:MM:SS DD Mmm YY, YYYY PST', null=True, blank=True)),
                ('subscr_effective', models.DateTimeField(help_text='HH:MM:SS DD Mmm YY, YYYY PST', null=True, blank=True)),
                ('subscr_id', models.CharField(max_length=19, blank=True)),
                ('username', models.CharField(max_length=64, blank=True)),
                ('case_creation_date', models.DateTimeField(help_text='HH:MM:SS DD Mmm YY, YYYY PST', null=True, blank=True)),
                ('case_id', models.CharField(max_length=14, blank=True)),
                ('case_type', models.CharField(max_length=24, blank=True)),
                ('receipt_id', models.CharField(max_length=64, blank=True)),
                ('currency_code', models.CharField(default='USD', max_length=32, blank=True)),
                ('handling_amount', models.DecimalField(default=0, null=True, max_digits=64, decimal_places=2, blank=True)),
                ('transaction_subject', models.CharField(max_length=255, blank=True)),
                ('ipaddress', models.IPAddressField(blank=True)),
                ('flag', models.BooleanField(default=False)),
                ('flag_code', models.CharField(max_length=16, blank=True)),
                ('flag_info', models.TextField(blank=True)),
                ('query', models.TextField(blank=True)),
                ('response', models.TextField(blank=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('from_view', models.CharField(max_length=6, null=True, blank=True)),
            ],
            options={
                'db_table': 'paypal_ipn',
                'verbose_name': 'PayPal IPN',
            },
            bases=(models.Model,),
        ),
    ]
