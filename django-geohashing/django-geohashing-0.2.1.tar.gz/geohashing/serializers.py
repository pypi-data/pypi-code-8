"""
Serializers for the geohashing app
"""

from rest_framework import serializers

from .models import Day


class DaySerializer(serializers.ModelSerializer):
    """
    ModelSerializer that exposes the useful fields on
    the Day model. Currently, every field is exposed
    except for the auto-incrementing PK (which is only
    present in the first place because every non-m2m table
    deserves a surrogate PK.
    """
    class Meta:
        model = Day
        fields = (
            'geohash_date',
            'djia_open',
            'latitude_delta',
            'longitude_delta',
            'djia_open_30w_adj',
            'latitude_delta_30w_adj',
            'longitude_delta_30w_adj',
        )
