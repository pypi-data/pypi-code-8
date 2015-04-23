from django.contrib import admin
from .models import *

class MenuAdmin(admin.ModelAdmin):
    list_display = ('name','position',)
    list_editable = ('position',)

admin.site.register(Menu, MenuAdmin)
