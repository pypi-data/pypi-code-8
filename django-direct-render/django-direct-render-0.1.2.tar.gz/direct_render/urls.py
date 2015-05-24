from django.conf.urls import url
from .views import direct_render


urlpatterns = [
    url('^(?P<template_name>.*\.html)$', direct_render)
]
