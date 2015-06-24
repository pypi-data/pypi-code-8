from django.db import models
from easy_thumbnails.fields import ThumbnailerImageField
from taggit.managers import TaggableManager


class Image(models.Model):
    file = ThumbnailerImageField(upload_to='media/%Y/%m')
    tags = TaggableManager()

    def __unicode__(self):
        return self.file.name
