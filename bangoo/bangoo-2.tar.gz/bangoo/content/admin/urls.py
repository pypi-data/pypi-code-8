from . import views
from django.conf.urls import patterns, url

urlpatterns = patterns('',
    url(r'^$', views.edit_content, name='admin-content-edit'),
)
