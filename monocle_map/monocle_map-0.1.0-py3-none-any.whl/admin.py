from django.contrib import admin
from .models import *

class MapAdmin(admin.ModelAdmin):
    list_display = ('name', 'mapType',)
    fields = ['name', 'map', 'zoom', 'markerImg', 'baloon', 'mapType']


admin.site.register(Map, MapAdmin)