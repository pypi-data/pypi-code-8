from django.contrib import admin
from .models import *
from django_summernote.admin import SummernoteModelAdmin

class ReviewAdmin(SummernoteModelAdmin):
    list_display = ('reviewer', 'position', 'isShown',)
    list_editable = ('position','isShown',)

admin.site.register(Review, ReviewAdmin)
