from django.conf.urls import patterns, url

import gumby
gumby.autodiscover()

urlpatterns = patterns('',
    url(r'^$', 'gumby.views.home', name='health_check'),
    url(r"^(?P<check_name>[\w\-]+)/$", 'gumby.views.check', name='health_check'),
)
