# coding: utf8
from django.conf import settings
from django.db import models
from django.utils.translation import ugettext_lazy as _

from hvad.models import TranslatableModel, TranslatedFields


class Content(TranslatableModel):
    is_page = models.BooleanField(default=True)
    authors = models.ManyToManyField(settings.AUTH_USER_MODEL, verbose_name=_('authors'))
    created = models.DateTimeField(verbose_name=_('created'), auto_now_add=True)
    published = models.DateTimeField(verbose_name=_('published'), blank=True, null=True)
    allow_comments = models.BooleanField(_('allow comments'), default=False)
    template_name = models.CharField(_('template name'), max_length=70, blank=True,
                                     help_text=_("Example: 'content/contact_page.html'. If this isn't provided, the "
                                                 "system will use 'content/default.html'."))
    registration_required = models.BooleanField(_('registration required'), default=False)
    translations = TranslatedFields(
        title=models.CharField(verbose_name=_('title'), max_length=255),
        url=models.CharField(verbose_name=_('url'), max_length=255),
        text=models.TextField(verbose_name=_('content'), blank=True),
        meta={
            'unique_together': [('url', 'language_code')],
            'permissions': (
                ('list_contents', 'Can list all content'),
            ),
        }
    )

# TODO: move to apps.py
from bangoo.navigation.signals import menu_created
from bangoo.content.receivers import menu_created_callback
menu_created.connect(menu_created_callback)
