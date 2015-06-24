from django.contrib import admin

from textplusstuff.admin import TextPlusStuffRegisteredModelAdmin

from .models import (
    StacksTextBlock,
    StacksTextBlockList,
    StacksTextBlockListTextBlock
)


class StacksTextBlockListTextBlockInline(admin.StackedInline):
    model = StacksTextBlockListTextBlock
    raw_id_fields = ('text_block',)


class StacksTextBlockAdmin(TextPlusStuffRegisteredModelAdmin):
    list_display = ('name', 'display_title', 'date_created', 'date_modified')


class StacksTextBlockListAdmin(TextPlusStuffRegisteredModelAdmin):
    inlines = [StacksTextBlockListTextBlockInline]
    list_display = ('name', 'display_title', 'date_created', 'date_modified')

admin.site.register(StacksTextBlock, StacksTextBlockAdmin)
admin.site.register(StacksTextBlockList, StacksTextBlockListAdmin)
