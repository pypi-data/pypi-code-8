from django.conf.urls import patterns, include, url

urlpatterns = patterns('touchnet.views',
    url(r'^postback$', 'postback', name='touchnet_postback'),
)
