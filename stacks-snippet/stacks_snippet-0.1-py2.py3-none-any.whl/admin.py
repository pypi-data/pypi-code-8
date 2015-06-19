from django.contrib import admin

from textplusstuff.admin import TextPlusStuffRegisteredModelAdmin

from .models import Snippet


class SnippetAdmin(TextPlusStuffRegisteredModelAdmin):
    search_fields = ['name']


admin.site.register(Snippet, SnippetAdmin)
