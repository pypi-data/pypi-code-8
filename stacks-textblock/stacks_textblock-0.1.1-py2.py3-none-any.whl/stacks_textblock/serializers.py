from rest_framework import serializers

from textplusstuff.serializers import (
    ExtraContextSerializerMixIn,
    TextPlusStuffFieldSerializer
)

from .models import StacksTextBlock, StacksTextBlockList


class StacksTextBlockSerializer(ExtraContextSerializerMixIn,
                                serializers.ModelSerializer):
    """Serializes StacksTextBlock instances."""

    content = TextPlusStuffFieldSerializer()

    class Meta:
        model = StacksTextBlock
        fields = (
            'name',
            'display_title',
            'content',
        )


class StacksTextBlockListSerializer(ExtraContextSerializerMixIn,
                                    serializers.ModelSerializer):
    text_blocks = serializers.SerializerMethodField()

    class Meta:
        model = StacksTextBlockList
        fields = ('name', 'display_title', 'text_blocks')

    def get_text_blocks(self, obj):
        """Order `images` field properly."""
        text_blocks = obj.text_blocks.order_by(
            'stackstextblocklisttextblock__order'
        )
        text_blocks = StacksTextBlockSerializer(text_blocks, many=True)
        return text_blocks.data
