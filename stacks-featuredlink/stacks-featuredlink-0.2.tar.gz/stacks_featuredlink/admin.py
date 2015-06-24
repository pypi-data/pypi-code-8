from django.contrib import admin

from textplusstuff.admin import TextPlusStuffRegisteredModelAdmin

from .models import (
    StacksFeaturedLink,
    StacksFeaturedLinkList,
    StacksFeaturedLinkListLink
)


class StacksFeaturedLinkAdmin(TextPlusStuffRegisteredModelAdmin):
    exclude = ('image_ppoi',)
    list_display = ('name', 'display_title', 'date_created', 'date_modified')
    search_fields = ('name', 'display_title')


class StacksFeaturedLinkListImageInline(admin.StackedInline):
    model = StacksFeaturedLinkListLink
    exclude = ('links',)
    raw_id_fields = ('link',)


class StacksFeaturedLinkListAdmin(TextPlusStuffRegisteredModelAdmin):
    inlines = [StacksFeaturedLinkListImageInline]
    list_display = ('name', 'display_title', 'date_created', 'date_modified')

admin.site.register(StacksFeaturedLink, StacksFeaturedLinkAdmin)
admin.site.register(StacksFeaturedLinkList, StacksFeaturedLinkListAdmin)
