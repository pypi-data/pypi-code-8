"""ORM models relating to publishing Mirrors Component objects and their
data."""

from django.db import models


class PublishReceipt(models.Model):
    """A receipt that indicates that a :class:`Component` has been published,
    when the publish was performed, and what specific revision of the Component
    was used.

    .. note :: Generally speaking this is an internal class and you probably
               don't need to muck about with it.

    """
    component = models.ForeignKey('mirrors.Component',
                                  related_name='publish_receipts')
    revision = models.ForeignKey('mirrors.ComponentRevision', related_name='+')

    publish_datetime = models.DateTimeField(auto_now_add=True)
