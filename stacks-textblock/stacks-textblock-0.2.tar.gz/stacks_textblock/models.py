from django.db import models
from django.utils.encoding import python_2_unicode_compatible
from django.utils.translation import ugettext_lazy as _

from textplusstuff.fields import TextPlusStuffField


class StacksTextBlockBase(models.Model):
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


@python_2_unicode_compatible
class StacksTextBlock(StacksTextBlockBase):
    """Represents a block of text."""

    content = TextPlusStuffField(
        _('Content'),
        help_text=_(
            "Enter the content of your Text Block here."
        )
    )

    class Meta:
        verbose_name = _('Text Block')
        verbose_name_plural = _('Text Blocks')

    def __str__(self):
        """Return the string representation of this textblock."""
        return self.name


@python_2_unicode_compatible
class StacksTextBlockList(StacksTextBlockBase):
    """Represents a list of StacksTextBlock instances."""

    text_blocks = models.ManyToManyField(
        StacksTextBlock,
        through='StacksTextBlockListTextBlock'
    )

    class Meta:
        verbose_name = _('Stacks Text Block List')
        verbose_name_plural = _('Stacks Text Block List')

    def __str__(self):
        return self.name


@python_2_unicode_compatible
class StacksTextBlockListTextBlock(models.Model):
    """
    A through table for connecting StacksTextBlock instances to
    StacksTextBlockList instances.
    """

    text_block_list = models.ForeignKey(
        'StacksTextBlockList'
    )
    order = models.PositiveIntegerField()
    text_block = models.ForeignKey(
        'StacksTextBlock'
    )

    class Meta:
        ordering = ('order',)

    def __str__(self):
        return "{} {}. {}".format(
            self.text_block_list.name,
            self.order,
            self.text_block.name,
        )
