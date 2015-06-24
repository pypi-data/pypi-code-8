from django.db import models

from ckeditor.fields import RichTextField
from jmbo.models import ModelBase


class Video(ModelBase):
    autosave_fields = ('content',)

    stream = models.URLField(max_length=255)
    content = RichTextField(
        blank=True,
        null=True,
    )

    class Meta:
        verbose_name = 'Video'
        verbose_name_plural = 'Videos'
