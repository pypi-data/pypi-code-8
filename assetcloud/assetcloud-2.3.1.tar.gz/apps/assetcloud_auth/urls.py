# (c) 2011 Bright Interactive Limited. All rights reserved.
# http://www.bright-interactive.com | info@bright-interactive.com

from django.conf.urls import patterns, url


urlpatterns = patterns('assetcloud_auth.views',
    url(r'^user/add/', 'user_add', name='user_add'),
    url(r'^user/update/(?P<id>\d+)/$', 'user_update',
        name='user_update'),
    url(r'^delete-user/(?P<id>\d+)/$', 'delete_user',
        name='delete-user'),
    url(r'^change-password/$', 'change_password', {'section': 'users'},
        name='change-password'),
    url(r'^login-as-user/(?P<id>\d+)/$', 'login_as_user', name='login-as-user'),
)
