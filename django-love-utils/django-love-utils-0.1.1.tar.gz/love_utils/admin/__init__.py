# -*- coding: utf-8 -*-

from __future__ import unicode_literals

from django.contrib import admin


class OrderableAdmin(admin.ModelAdmin):
    list_display = list_editable = exclude = ('position',)

    class Meta:
        abstract = True

    class Media:
        js = (
            'love_utils/js/orderable.js',
        )