from django.db import models
from django.utils.translation import ugettext_lazy as _


class Snippet(models.Model):
    """Represents a snippet of HTML."""
    date_created = models.DateTimeField(
        auto_now_add=True
    )
    date_modified = models.DateTimeField(
        auto_now=True
    )
    name = models.CharField(
        _('Name'),
        max_length=100,
        help_text=_("The name of this HTML snippet. For internal use only.")
    )
    display_title = models.CharField(
        _('Display Title'),
        max_length=100,
        help_text=_(
            'An optional displayed-to-the-user title of this content.'
        ),
        blank=True
    )
    snippet = models.TextField(
        _('HTML Snippet'),
        help_text=_("The snippet of HTML.")
    )

    def __unicode__(self):
        return self.name
