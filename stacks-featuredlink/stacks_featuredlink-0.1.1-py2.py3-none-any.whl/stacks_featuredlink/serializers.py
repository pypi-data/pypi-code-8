from __future__ import unicode_literals

from django.conf import settings

from rest_framework import serializers
from textplusstuff.serializers import (
    ExtraContextSerializerMixIn,
    TextPlusStuffFieldSerializer
)
from versatileimagefield.serializers import VersatileImageFieldSerializer

from .models import StacksFeaturedLink, StacksFeaturedLinkList

image_sets = getattr(
    settings,
    'VERSATILEIMAGEFIELD_RENDITION_KEY_SETS',
    {}
).get(
    'stacks_featuredlink',
    [
        ('full_size', 'url'),
        ('gallery_thumb', 'crop__400x225'),
        ('3up_thumb', 'crop__700x394'),
        ('2up_thumb', 'crop__800x450'),
        ('full_width', 'crop__1600x901'),
    ]
)


class StacksFeaturedLinkSerializer(ExtraContextSerializerMixIn,
                                   serializers.ModelSerializer):
    """Serializes StacksFeaturedLink instances."""

    image = VersatileImageFieldSerializer(
        sizes=image_sets
    )
    optional_content = TextPlusStuffFieldSerializer()

    class Meta:
        model = StacksFeaturedLink
        fields = (
            'name',
            'display_title',
            'url',
            'image',
            'optional_content',
        )


class StacksFeaturedLinkListSerializer(ExtraContextSerializerMixIn,
                                       serializers.ModelSerializer):
    """Serializes StacksFeaturedLinkList instances."""
    links = serializers.SerializerMethodField()

    class Meta:
        model = StacksFeaturedLinkList
        fields = ('name', 'display_title', 'links')

    def get_links(self, obj):
        """Order `links` field properly."""
        links = obj.links.order_by('stacksfeaturedlinklistlink__order')
        links = StacksFeaturedLinkSerializer(links, many=True)
        return links.data
