from django.contrib import admin
from .models import *
from grappelli.forms import GrappelliSortableHiddenMixin

class SlideInline(GrappelliSortableHiddenMixin, admin.TabularInline):
    model = Slide
    sortable_field_name = "position"
    extra = 0

    fieldsets = [
        ('Настройки слайда', {'fields': ['name', 'image', 'text'], 'classes': ['collapse']}),
        ('Дополнительно', {'fields': ['isShown', 'position'], 'classes': ['collapse']}),
    ]
    list_display = ('name', 'image_admin', 'text', 'position', 'isShown',)

class SliderAdmin(admin.ModelAdmin):
    list_display = ('name', 'text', 'position','isShown', 'elem_number')
    list_editable = ('position','isShown',)
    inlines = [SlideInline]

    class Media:
        '''
        js = [
            '/static/grappelli/tinymce/jscripts/tiny_mce/tiny_mce.js',
            '/static/grappelli/tinymce_setup/tinymce_setup.js',
        ]
        '''

admin.site.register(Slider, SliderAdmin)
