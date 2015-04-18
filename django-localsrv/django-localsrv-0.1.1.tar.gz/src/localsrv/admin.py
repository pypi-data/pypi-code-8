from django.contrib import admin

from .forms import FilePickerForm
from .models import (ServableContent, StringSource, Source,
                     ServableHttpHeader, FileSource, URLSource)

# Register your models here.


class FileSourceAdmin(admin.ModelAdmin):
    form = FilePickerForm

admin.site.register(ServableContent)
admin.site.register(FileSource, FileSourceAdmin)
admin.site.register(StringSource)
admin.site.register(URLSource)
admin.site.register(ServableHttpHeader)