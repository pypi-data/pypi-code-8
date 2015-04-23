from rest_framework import serializers

from .models import Day


class DaySerializer(serializers.ModelSerializer):
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
