from django.contrib import admin
from .models import *

from django_summernote.admin import SummernoteModelAdmin

class TimerAdmin(SummernoteModelAdmin):
    list_display = ('text','deadline','isShown',)
    list_editable = ('deadline', 'isShown',)

admin.site.register(Timer, TimerAdmin)
