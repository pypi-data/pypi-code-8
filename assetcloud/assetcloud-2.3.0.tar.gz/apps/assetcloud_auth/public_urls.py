# (c) 2011 Bright Interactive Limited. All rights reserved.
# http://www.bright-interactive.com | info@bright-interactive.com

from django.conf.urls import patterns, url

urlpatterns = patterns('assetcloud_auth.views',
    url(r'^register/$', 'register', name='register'),
    url(r'^login/$', 'login', name='login'),
    url(r'^logout/$', 'logout', name='logout'),
    url(r'^activate/(?P<key>.+)/$', 'activate_user', name='activate-user'),
    url(r'^forgotten-password/', 'forgotten_password',
        name='forgotten-password'),
    url(r'^email-sent/$', 'forgotten_password_email_sent',
        name='forgotten-password-email-sent'),
    url(r'^password-reset/(?P<key>.+)/$', 'password_reset',
        name='password-reset'),
    url(r'^complete_profile/(?P<user_id>\d+)/(?P<key>.+)/$', 'complete_profile',
        name='complete_profile_action'),
    url(r'^social-associate/(?P<backend>.*)/(?P<user_id>\d+)/(?P<key>.+)/$', 'social_associate', name='social_associate_action'),
    url(r'^social-register/(?P<backend>.*)/$', 'social_register', name='social_register_action'),
    url(r'^social-login/(?P<backend>.*)/$', 'social_login', name='social_login_action'),
    url(r'^subdomain-check/$', 'subdomain_available',
        name='subdomain_available'),
)
