# (c) 2011 Bright Interactive Limited. All rights reserved.
# http://www.bright-interactive.com | info@bright-interactive.com

from django.conf.urls import patterns, url

urlpatterns = patterns('assetcloud.views',
    url(r'^share/(?P<share_id>\d+)/(?P<key>.+)/$', 'share', name='share'),
    url(r'^share/(?P<share_id>\d+)/(?P<key>.+)/(?P<asset_id>\d+)/download$',
        'shared_asset_download_action', name='shared_asset_download_action'),

)
