try:
    from django.core.exceptions import ImproperlyConfigured as ImproperlyConfiguredBase
except ImportError:
    ImproperlyConfiguredBase = Exception

class ImproperlyConfigured(ImproperlyConfiguredBase):
    pass
