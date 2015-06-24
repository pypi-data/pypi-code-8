from . import views
from django.conf.urls import url, patterns

urlpatterns = patterns('',
    url(r'', views.menu_dispatcher),
)