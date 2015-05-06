from django.contrib import admin
from .models import *
from grappelli.forms import GrappelliSortableHiddenMixin

from django_summernote.admin import SummernoteModelAdmin
from django_summernote.admin import SummernoteInlineModelAdmin

class SlideInline(GrappelliSortableHiddenMixin, admin.TabularInline, SummernoteInlineModelAdmin):
    model = Slide
    sortable_field_name = "position"
    extra = 0

    fieldsets = [
        ('Настройки слайда', {'fields': ['name', 'image', 'text'], 'classes': ['collapse']}),
        ('Дополнительно', {'fields': ['position', 'isShown'], 'classes': ['collapse']}),
    ]
    list_display = ('name', 'text', 'position',)

class SliderAdmin(SummernoteModelAdmin):
    list_display = ('name', 'elem_number', 'isShown',)
    list_editable = ('elem_number', 'isShown',)
    inlines = [SlideInline]

admin.site.register(Slider, SliderAdmin)
