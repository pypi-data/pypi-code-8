from django.conf import settings
from django.conf.urls.static import static
from django.conf.urls import *
from cmsplugin_latest.views import CMSPluginLatestFeed

urlpatterns = patterns('',
    url(r'^modellatest/$', 'cmsplugin_latest.views.index', name='index'),
    url(r'^modellatest/getmodelfields/$',
        'cmsplugin_latest.views.get_model_fields',
        name="get_model_fields"),

#    url(r'^modellatest/feeds/$',
#        CMSPluginLatestFeed()),
#    url(r'^modellatest/feeds/(?P<model_name>[\w_]+)/$',
#        CMSPluginLatestFeed()),
#    url(r'^modellatest/feeds/(?P<model_name>[\w_\d]+)/$(?P<model_pk>[\d]+$',
#        CMSPluginLatestFeed()),
)
