__title__ = 'fobi.contrib.apps.djangocms_integration.models'
__author__ = 'Artur Barseghyan <artur.barseghyan@gmail.com>'
__copyright__ = 'Copyright (c) 2014 Artur Barseghyan'
__license__ = 'GPL 2.0/LGPL 2.1'
__all__ = ('FobiFormWidget',)

from django.db import models
from django.utils.translation import ugettext_lazy as _

from cms.models import CMSPlugin

try:
    from cms.utils.compat.dj import python_2_unicode_compatible
except ImportError:
    from django.utils.encoding import python_2_unicode_compatible

from fobi.contrib.apps.djangocms_integration.helpers import (
    get_form_template_choices, get_success_page_template_choices
)

@python_2_unicode_compatible
class FobiFormWidget(CMSPlugin):
    """
    Plugin for storing ``django-fobi`` form reference.
    """
    form_entry = models.ForeignKey('fobi.FormEntry', verbose_name=_("Form"))

    form_template_name = models.CharField(
        _("Form template name"), max_length=255, null=True, blank=True,
        choices=get_form_template_choices(),
        help_text=_("Template to render the form with.")
        )

    hide_form_title = models.BooleanField(
        _("Hide form title"), default=False,
        help_text=_("If checked, no form title is shown.")
        )

    form_title = models.CharField(
        _("Form title"), max_length=255, null=True, blank=True,
        help_text=_("Overrides the default form title.")
        )

    form_submit_button_text = models.CharField(
        _("Submit button text"), max_length=255, null=True, blank=True,
        help_text=_("Overrides the default form submit button text.")
        )

    success_page_template_name = models.CharField(
        _("Success page template name"), max_length=255, null=True, blank=True,
        choices=get_success_page_template_choices(),
        help_text=_("Template to render the success page with.")
        )

    hide_success_page_title = models.BooleanField(
        _("Hide success page title"), default=False,
        help_text=_("If checked, no success page title is shown.")
        )

    success_page_title = models.CharField(
        _("Succes page title"), max_length=255, null=True, blank=True,
        help_text=_("Overrides the default success page title.")
        )

    success_page_text = models.TextField(
        _("Succes page text"), null=True, blank=True,
        help_text=_("Overrides the default success page text.")
        )

    def __str__(self):
        return self.form_entry.name

    search_fields = ('form_entry__name',)
