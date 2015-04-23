import datetime

from django.shortcuts import render

from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response

from .models import Day
from .serializers import DaySerializer

@api_view(['GET',])
def get_geohash(request, year, month, day, format=None):
    """
    Return the geohash for a given day if we have a record for it.

    Will return '400 Bad Request' if year, month and day don't 
    combine to form a valid date.

    Will return '404 Not Found' if geohash data for this date is not found.
    """
    try:
        year = int(year)
        month = int(month)
        day = int(day)
        geohash_date = datetime.date(year, month, day)
    except ValueError, TypeError:
        return Response(status=status.HTTP_400_BAD_REQUEST)

    try:
        geohash = Day.objects.get(geohash_date=geohash_date)
    except Day.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    serializer = serializers.DaySerializer(geohash)
    return Response(serializer.data)
