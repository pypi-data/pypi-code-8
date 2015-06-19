from django.utils.safestring import mark_safe

from rest_framework import serializers
from textplusstuff.serializers import ExtraContextSerializerMixIn

from .models import Snippet


class SnippetSerializer(ExtraContextSerializerMixIn,
                        serializers.ModelSerializer):
    snippet = serializers.SerializerMethodField()

    class Meta:
        model = Snippet
        fields = (
            'name',
            'snippet'
        )

    def get_snippet(self, obj):
        return mark_safe(obj.snippet)
