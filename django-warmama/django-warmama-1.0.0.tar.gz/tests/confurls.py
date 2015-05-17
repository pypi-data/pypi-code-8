"""Urls module for test project"""
from django.conf.urls import include, url


urlpatterns = [
    url(r'^', include('warmama.urls', namespace='warmama-instance', app_name='warmama')),
]
