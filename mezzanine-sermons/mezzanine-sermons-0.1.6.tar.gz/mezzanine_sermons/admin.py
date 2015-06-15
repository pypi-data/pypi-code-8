from __future__ import unicode_literals

from django.contrib import admin

from mezzanine_sermons.models import SermonSeries, Sermon, SermonFile


class SermonSeriesAdmin(admin.ModelAdmin):
    search_fields = ['title', 'bible_passage', 'description']


class SermonFileInline(admin.StackedInline):
    model = SermonFile
    verbose_name = "File"
    verbose_name_plural = "Files"


class SermonAdmin(admin.ModelAdmin):
    search_fields = ['series__title', 'series__bible_passage', 'series__description', 'title', 'passage', 'preacher']
    inlines = [SermonFileInline, ]


admin.site.register(SermonSeries, SermonSeriesAdmin)
admin.site.register(Sermon, SermonAdmin)

