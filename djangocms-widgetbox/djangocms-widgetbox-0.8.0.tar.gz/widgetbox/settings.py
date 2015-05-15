from django.conf import settings


GALLERY_STYLES = getattr(
    settings, 'WIDGETBOX_GALLERY_STYLES',
    (('default', 'default'),)
)

