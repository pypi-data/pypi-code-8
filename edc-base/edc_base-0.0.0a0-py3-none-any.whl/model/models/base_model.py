import socket

from django.core.urlresolvers import reverse
from django.db import models

from django_extensions.db.models import TimeStampedModel

from django_revision import RevisionField

from ..constants import BASE_MODEL_UPDATE_FIELDS
from ..fields import HostnameModificationField


class BaseModel(TimeStampedModel):

    """Base model class for all models. Adds created and modified'
    values for user, date and hostname (computer)."""

    user_created = models.CharField(
        max_length=50,
        verbose_name='user created',
        editable=False,
        default="",
        db_index=True,
        help_text="System field. (updated by admin)"
    )

    user_modified = models.CharField(
        max_length=50,
        verbose_name='user modified',
        editable=False,
        default="",
        db_index=True,
        help_text="System field. (updated by admin)",
    )

    hostname_created = models.CharField(
        max_length=50,
        editable=False,
        default=socket.gethostname(),
        db_index=True,
        help_text="System field. (modified on create only)",
    )

    hostname_modified = HostnameModificationField(
        max_length=50,
        editable=False,
        default=socket.gethostname(),
        db_index=True,
        help_text="System field. (modified on every save)",
    )

    revision = RevisionField(
        help_text="System field. Git repository tag:branch:commit."
    )

    def save(self, *args, **kwargs):
        try:
            # don't allow update_fields to bypass these audit fields
            update_fields = kwargs.get('update_fields', None) + BASE_MODEL_UPDATE_FIELDS
            kwargs.update({'update_fields': update_fields})
        except TypeError:
            pass
        super(BaseModel, self).save(*args, **kwargs)

    def get_absolute_url(self):
        if self.id:
            url = reverse('admin:{app_label}_{object_name}_change'.format(
                app_label=self._meta.app_label,
                object_name=self._meta.object_name.lower()
            ), args=(self.id,))
        else:
            url = reverse('admin:{app_label}_{object_name}_add'.format(
                app_label=self._meta.app_label,
                object_name=self._meta.object_name.lower())
            )
        return url

    class Meta:
        abstract = True
