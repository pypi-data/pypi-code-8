# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import feincms.translations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Person',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('title_prefix', models.CharField(help_text='Nap\u0159\xedklad: Ing.', max_length=127, verbose_name='Titul p\u0159ed jm\xe9nem', blank=True)),
                ('first_name', models.CharField(help_text='Nap\u0159\xedklad: Martin', max_length=127, verbose_name='Jm\xe9no')),
                ('last_name', models.CharField(help_text='Nap\u0159\xedklad: Kocourek', max_length=127, verbose_name='P\u0159\xedjmen\xed')),
                ('title_suffix', models.CharField(help_text='Nap\u0159\xedklad: PhD.', max_length=127, verbose_name='Titul za jm\xe9nem', blank=True)),
                ('nick_name', models.SlugField(help_text='Nap\u0159\xedklad: fanda', max_length=127, verbose_name='Nickname')),
                ('email', models.EmailField(help_text='P\u0159.: martin.kocourek@contractis.cz', max_length=75, verbose_name='E-mail', blank=True)),
                ('photo', models.ImageField(help_text='Pou\u017eijte obr\xe1zky ve form\xe1tu JPEG, GIF nebo PNG. Obr\xe1zky se automaticky zmen\u0161\xed na po\u017eadovan\xfd rozm\u011br.', upload_to=b'team', verbose_name='Fotografie', blank=True)),
                ('category', models.CharField(default=b'1', help_text='Pro \u010dlen\u011bn\xed na str\xe1nce.', max_length=127, verbose_name='Kategorie', choices=[(b'0', '0'), (b'1', '1')])),
                ('sort_order', models.PositiveIntegerField(help_text='Nepovinn\xfd \xfadaj pro mo\u017enost vlastn\xedho \u0159azen\xed. Pokud m\xe1 v\xedce zam\u011bstnanc\u016f stejn\xe9 po\u0159adov\xe9 \u010d\xedslo, \u0159ad\xed se zam\u011bstnanci abecedn\u011b dle p\u0159\xedjmen\xed.', null=True, verbose_name='Po\u0159ad\xed', blank=True)),
                ('active', models.BooleanField(default=True, help_text='Neaktivn\xed karty zam\u011bstnance se nezobraz\xed na str\xe1nce.', verbose_name='Je aktivn\xed?')),
            ],
            options={
                'ordering': ['sort_order', 'last_name'],
                'verbose_name': 'Team member',
                'verbose_name_plural': 'Team members',
            },
            bases=(models.Model, feincms.translations.TranslatedObjectMixin),
        ),
        migrations.CreateModel(
            name='PersonContact',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('engine', models.CharField(blank=True, max_length=255, verbose_name='Type', choices=[(b'facebook', 'Facebook'), (b'linkedin', 'LinkedIn'), (b'twitter', 'Twitter'), (b'github', 'Github')])),
                ('url', models.URLField(verbose_name='url', blank=True)),
                ('person', models.ForeignKey(related_name='contacts', verbose_name='person', to='team.Person')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='PersonTranslation',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('language_code', models.CharField(default=b'en', max_length=10, verbose_name='language', choices=[(b'en', b'EN'), (b'cs', b'CS')])),
                ('position', models.CharField(max_length=250, verbose_name='position', blank=True)),
                ('summary', models.TextField(null=True, verbose_name='top text', blank=True)),
                ('description', models.TextField(null=True, verbose_name='bottom text', blank=True)),
                ('parent', models.ForeignKey(related_name='translations', to='team.Person')),
            ],
            options={
                'verbose_name': 'text',
                'verbose_name_plural': 'texts',
            },
            bases=(models.Model,),
        ),
    ]
