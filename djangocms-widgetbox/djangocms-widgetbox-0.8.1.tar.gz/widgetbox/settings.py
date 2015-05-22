from django.conf import settings


GALLERY_STYLES = getattr(
    settings, 'WIDGETBOX_GALLERY_STYLES',
    (('default', 'default'),)
)

FAQ_STYLES = getattr(
    settings, 'WIDGETBOX_FAQ_STYLES',
    (('widgetbox/faq-topic.html', 'Default'),)
)

