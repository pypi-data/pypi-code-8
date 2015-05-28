# -*- coding: utf-8 -*-
from django.conf.urls import patterns, url
from . import views

urlpatterns = patterns('',
    url(r'^list/$', views.SponsorsList.as_view(), name='list-sponsors'),
)
