from django.conf.urls import patterns, include
from django.contrib import admin


admin.autodiscover()

urlpatterns = patterns(
    '',
    (r'^atlas/', include('atlas.urls')),
    (r'^admin/', include(admin.site.urls)),
)
