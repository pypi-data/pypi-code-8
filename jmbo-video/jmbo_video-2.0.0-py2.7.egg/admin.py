from django.contrib import admin

from jmbo.admin import ModelBaseAdmin
from video.models import Video


admin.site.register(Video, ModelBaseAdmin)
