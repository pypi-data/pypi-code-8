from django.conf.urls import patterns, url
from .router import route_factory

urlpatterns = patterns('',
    url(r'^(\S+)', route_factory, name='router'),
    url(r'^', route_factory, name='router_root'),
)
