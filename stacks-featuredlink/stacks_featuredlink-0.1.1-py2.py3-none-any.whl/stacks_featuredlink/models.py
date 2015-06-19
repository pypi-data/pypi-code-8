from django.db import models
from django.utils.encoding import python_2_unicode_compatible
from django.utils.translation import ugettext_lazy as _

from textplusstuff.fields import TextPlusStuffField
from versatileimagefield.fields import VersatileImageField, PPOIField


class StacksFeaturedLinkBase(models.Model):
    """
    An abstract base model that keeps track of when a model instance
    was created and last-updated.
    """

    date_created = models.DateTimeField(
        auto_now_add=True
    )
    date_modified = models.DateTimeField(
        auto_now=True
    )
    name = models.CharField(
        _('Name'),
        max_length=100,
        help_text=_('The internal name/signifier of this content.')
    )
    display_title = models.CharField(
        _('Display Title'),
        max_length=100,
        help_text=_(
            'An optional displayed-to-the-user title of this content.'
        ),
        blank=True
    )

    class Meta:
        abstract = True
        ordering = ('-date_modified', '-date_created')


@python_2_unicode_compatible
class StacksFeaturedLink(StacksFeaturedLinkBase):
    """Represents an featured link."""

    url = models.URLField(
        _('URL'),
        max_length=300,
        blank=True
    )
    image = VersatileImageField(
        upload_to='stacks_featuredlink/',
        ppoi_field='image_ppoi',
        blank=True
    )
    image_ppoi = PPOIField()
    optional_content = TextPlusStuffField(
        _('Optional Content'),
        blank=True,
        help_text=_(
            "A field to enter optional accompanying content."
        )
    )

    class Meta:
        verbose_name = _('Stacks Featured Link')
        verbose_name_plural = _('Stacks Featured Links')

    def __str__(self):
        return self.name


@python_2_unicode_compatible
class StacksFeaturedLinkList(StacksFeaturedLinkBase):
    """Represents a list of StacksFeaturedLink instances."""

    links = models.ManyToManyField(
        StacksFeaturedLink,
        through='StacksFeaturedLinkListLink'
    )

    class Meta:
        verbose_name = _('Stacks Featured Link List')
        verbose_name_plural = _('Stacks Featured Link Lists')

    def __str__(self):
        return self.name


@python_2_unicode_compatible
class StacksFeaturedLinkListLink(models.Model):
    """
    A through table for connecting StacksFeaturedLink instances to
    StacksFeaturedLinkList instances.
    """
    link_list = models.ForeignKey(
        StacksFeaturedLinkList
    )
    order = models.PositiveIntegerField()
    link = models.ForeignKey(
        StacksFeaturedLink
    )

    class Meta:
        ordering = ('order',)

    def __str__(self):
        return "{} {}. {}".format(
            self.link_list.name,
            self.order,
            self.link.name,
        )
