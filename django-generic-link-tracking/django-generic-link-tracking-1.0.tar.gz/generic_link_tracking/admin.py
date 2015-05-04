from django.contrib import admin
from .models import GenericLink


class GenericLinkAdmin(admin.ModelAdmin):
    list_display = ('url', 'click_count', 'link')
    list_filter = ('show_in_admin',)
    fields = ('where', 'url', )
admin.site.register(GenericLink, GenericLinkAdmin)
