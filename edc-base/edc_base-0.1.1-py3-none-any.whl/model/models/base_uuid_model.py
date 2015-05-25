import uuid

from django.db import models

from .base_model import BaseModel


class BaseUuidModel(BaseModel):

    """Base model class for all models using an UUID and not an INT for the primary key. """

    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False,
        help_text="System field. UUID primary key.")

    class Meta:
        abstract = True
