# -*- coding: utf-8 -*-

from django.conf import settings
from django import forms
from django.forms.models import modelformset_factory
from django.contrib import admin
from django.utils.translation import ugettext as _

from sorl.thumbnail import get_thumbnail

from .models import Person, PersonTranslation, PersonContact


class PersonTranslation_Inline(admin.StackedInline):
    model = PersonTranslation
    max_num = len(settings.LANGUAGES)


def thumb(object):
    if object.photo:
        thumb = get_thumbnail(object.photo, '50x50', format='PNG')
        return "<img src='%s' alt='' />" % thumb.url
    else:
        return 'N/A'
thumb.short_description = _('preview')
thumb.allow_tags = True


class PersonContact_Inline(admin.StackedInline):
    model = PersonContact


class PersonAdmin(admin.ModelAdmin):
    list_display = ['full_name', 'category', thumb, 'sort_order', 'active', ]
    list_filter = ('active', 'category')
    list_editable = ('sort_order', 'active',)
    inlines = [PersonTranslation_Inline, PersonContact_Inline]

admin.site.register(Person, PersonAdmin)
