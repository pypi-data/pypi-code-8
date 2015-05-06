from django.contrib import admin
from .models import *
from django_summernote.admin import SummernoteModelAdmin

class MapAdmin(SummernoteModelAdmin):
    list_display = ('name', 'mapType',)
    list_editable = ('mapType',)

    fieldsets = [
        ('Название', {'fields': ['name',]}),
        ('Метка', {'fields': ['map', 'markerImg', 'baloon', ]}),
        ('Настройки карты', {'fields': ['zoom', 'mapDisplayType', 'mapType', ], 'classes': ['collapse']}),
    ]

admin.site.register(Map, MapAdmin)