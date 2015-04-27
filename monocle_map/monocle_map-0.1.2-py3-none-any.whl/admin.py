from django.contrib import admin
from .models import *

class MapAdmin(admin.ModelAdmin):
    list_display = ('name', 'mapType',)
    fields = ['name', 'map', 'zoom', 'markerImg', 'baloon', 'mapType']

    class Media:
        '''
        js = [
            '/static/grappelli/tinymce/jscripts/tiny_mce/tiny_mce.js',
            '/static/grappelli/tinymce_setup/tinymce_setup.js',
        ]
        '''


admin.site.register(Map, MapAdmin)