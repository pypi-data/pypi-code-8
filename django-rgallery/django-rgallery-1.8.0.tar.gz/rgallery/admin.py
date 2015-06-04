# -*- coding: utf-8 -*-

from django.contrib import admin
from django.utils.safestring import mark_safe

import models as mymodels

from engine import expire_view_cache
from sorl.thumbnail import get_thumbnail


class FolderAdminForm(admin.ModelAdmin):
    prepopulated_fields = {'slug': ['title']}


class PhotoAdminForm(admin.ModelAdmin):
    list_display = ('thumb', 'image', 'folder', 'capture_date')
    search_fields = ('image', 'origen', )
    ordering = ('-capture_date', )

    def thumb(self, obj):
        try:
            if obj.image:
                tb = get_thumbnail(obj.image, "60x60")
                return mark_safe('<img width="%s" src="%s" />') % (tb.width,
                                                                   tb.url)
            else:
                return "No image"
        except:
            return "No Image"

    thumb.short_description = 'Photo Thumb'
    thumb.allow_tags = True

    def save_model(self, request, obj, form, change):
        fake_metas = {'HTTP_HOST': request.META['HTTP_HOST'],
                      'SERVER_PORT': request.META['SERVER_PORT']}
        expire_view_cache("app_gallery-gallery", fake_metas)
        folders = mymodels.Folder.objects.all()
        if folders is not None:
            for f in folders:
                expire_view_cache("app_gallery-folder", fake_metas, [f.slug])
        obj.save()


admin.site.register(mymodels.Photo, PhotoAdminForm)
admin.site.register(mymodels.Folder, FolderAdminForm)
