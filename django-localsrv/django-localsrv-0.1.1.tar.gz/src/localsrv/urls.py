from django.conf.urls import url
from .views import serve_all

urlpatterns = (
    url(r'^.*$', serve_all, name="localsrv:serve_all"),
)