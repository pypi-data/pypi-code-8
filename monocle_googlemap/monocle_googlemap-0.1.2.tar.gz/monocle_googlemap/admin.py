from django.contrib import admin
from .models import *

class GoogleMapAdmin(admin.ModelAdmin):
    list_display = ('name','map',)

admin.site.register(GoogleMap, GoogleMapAdmin)
