from django.conf.urls import patterns, url
from .views import *

urlpatterns = patterns('',
                url(r'^sites/',SiteList.as_view()),
                url(r'^signature/',SignatureList.as_view()),

)