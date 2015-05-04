from django.db import models
try:
    from django.contrib.contenttypes.fields import GenericForeignKey
except ImportError:
    from django.contrib.contenttypes.generic import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.conf import settings
from django.utils.html import mark_safe
import numconv


class GenericLink(models.Model):
    where = models.CharField(max_length=200, blank=True, default="")
    url = models.URLField(max_length=255)
    created = models.DateTimeField(auto_now_add=True)
    show_in_admin = models.BooleanField(default=True)
    rotate = models.CharField(max_length=100, blank=True)  # comma separated IDs

    content_type = models.ForeignKey(ContentType, null=True, blank=True)
    object_id = models.PositiveIntegerField(null=True, blank=True)
    content_object = GenericForeignKey('content_type', 'object_id')

    def __unicode__(self):
        return self.url

    def get_link(self):
        quick_id = numconv.int2str(int(self.id), 32, numconv.BASE32)
        return "/glc/%s/" % quick_id

    def link(self):
        link = self.get_link()
        return mark_safe("<a href='%s'>%s</a>" % (link, link))

    def get_full_url(self):
        return settings.DOMAIN + self.get_link()

    @property
    def click_count(self):
        return GenericLinkClick.objects.filter(link=self).count()


class GenericLinkClick(models.Model):
    link = models.ForeignKey('GenericLink')
    ip = models.GenericIPAddressField()
    created = models.DateTimeField(auto_now_add=True)
