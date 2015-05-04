from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^glc/(?P<quick_id>[a-zA-Z0-9]+)/$', views.generic_link_click, name="generic_link_click"),
]
