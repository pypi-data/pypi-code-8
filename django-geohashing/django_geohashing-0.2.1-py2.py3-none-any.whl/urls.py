"""
URL routing for the geohashing app
"""

from django.conf.urls import url

from rest_framework.urlpatterns import format_suffix_patterns

from . import views

urlpatterns = [
    url(
        r'^(?P<year>\d{4})-(?P<month>\d{1,2})-(?P<day>\d{1,2})$',
        views.get_geohash,
        name='geohash'
    ),
]

urlpatterns = format_suffix_patterns(urlpatterns)

