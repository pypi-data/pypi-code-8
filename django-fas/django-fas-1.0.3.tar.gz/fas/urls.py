from django.conf.urls import patterns, url

from .views import login, complete, logout

urlpatterns = patterns('',
    url(r'^login/$',    login,      name='fas-login'),
    url(r'^complete/$', complete,   name='fas-complete'),
    url(r'^logout/$',   logout,     name='fas-logout'),
)
