# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin

from .models import Sponsor


class CustomSponsor(admin.ModelAdmin):
    list_display = ['id', 'enabled', 'name', 'width', 'height', 'does_expire', 'expires_on', 'category', ]
    list_editable = ['enabled', 'name', 'width', 'height', 'does_expire', 'expires_on', 'category', ]
    list_filter = ['enabled', 'does_expire', 'category', ]
    list_display_links = ['id', ]
    # readonly_fields = ['', ]
    # search_fields = ['', ]

admin.site.register(Sponsor, CustomSponsor)
