from django.contrib import admin
from .models import *

class MenuAdmin(admin.ModelAdmin):
    list_display = ('name', 'anchor', 'position', )
    list_editable = ('position', 'anchor', )

admin.site.register(Menu, MenuAdmin)
