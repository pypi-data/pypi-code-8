from django.utils.encoding import python_2_unicode_compatible

from django.db import models
from .settings import GALLERY_STYLES

from cms.models import CMSPlugin
from cms.models.fields import PageField

from djangocms_text_ckeditor.fields import HTMLField
from filer.fields.image import FilerImageField


@python_2_unicode_compatible
class ButtonPlugin(CMSPlugin):
    title = models.CharField(max_length=200)
    subtitle = models.CharField(max_length=200, blank=True)
    link_to_page = PageField(null=True, blank=True)
    link_custom = models.CharField(max_length=400, blank=True)
    icon = models.CharField(max_length=50, blank=True)

    class Meta:
        db_table = 'widgetbox_buttons'

    def __str__(self):
        return self.title


@python_2_unicode_compatible
class QuotePlugin(CMSPlugin):
    content = HTMLField()
    name = models.CharField(max_length=200)
    link = models.CharField(max_length=400, blank=True)
    image = FilerImageField(null=True, blank=True)

    class Meta:
        db_table = 'widgetbox_quotes'

    def __str__(self):
        return self.name


@python_2_unicode_compatible
class GalleryPlugin(CMSPlugin):
    style = models.CharField(
        max_length=100,
        choices=GALLERY_STYLES,
        default=GALLERY_STYLES[0][0]
    )

    class Meta:
        db_table = 'widgetbox_galleries'

    def __str__(self):
        return u'Gallery ({})'.format(self.style)

    def get_html_id(self):
        return u'gallery-{}'.format(self.pk)


@python_2_unicode_compatible
class GalleryImagePlugin(CMSPlugin):
    image = FilerImageField()
    title = models.CharField(max_length=100, blank=True)
    description = models.CharField(max_length=200, blank=True)

    class Meta:
        db_table = 'widgetbox_gallery_images'

    def __str__(self):
        return str(self.image)

    def get_title(self):
        return self.title or self.image.label

    def get_description(self):
        return self.description or self.image.description
