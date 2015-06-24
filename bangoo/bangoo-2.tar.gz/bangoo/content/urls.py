from .views import page
from django.conf.urls import url, patterns

urlpatterns = patterns('',
    url(r'', page),
)
