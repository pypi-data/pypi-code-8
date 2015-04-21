from django.contrib import admin
from .models import *

class YandexMapAdmin(admin.ModelAdmin):
    list_display = ('name','map',)

admin.site.register(YMap, YandexMapAdmin)
