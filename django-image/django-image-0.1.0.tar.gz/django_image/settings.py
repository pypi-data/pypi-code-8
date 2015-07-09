from django.conf import settings
from django.utils.module_loading import import_string

IMAGES_BACKEND = import_string(getattr(settings, 'IMAGES_BACKEND'))()
