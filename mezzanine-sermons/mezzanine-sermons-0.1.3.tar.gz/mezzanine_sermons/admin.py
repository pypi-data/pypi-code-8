from __future__ import unicode_literals

from django.contrib import admin

from mezzanine_sermons.models import SermonSeries, Sermon, SermonFile


class SermonSeriesAdmin(admin.ModelAdmin):
    pass


class SermonFileInline(admin.StackedInline):
    model = SermonFile
    verbose_name = "File"
    verbose_name_plural = "Files"


class SermonAdmin(admin.ModelAdmin):
    search_fields = ['series', 'title', 'passage', 'preacher']
    inlines = [SermonFileInline, ]


admin.site.register(SermonSeries, SermonSeriesAdmin)
admin.site.register(Sermon, SermonAdmin)

