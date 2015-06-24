from django.conf.urls import patterns, include
from django.contrib import admin


admin.autodiscover()

urlpatterns = patterns(
    '',
    (r'^jmbo/', include('jmbo.urls')),
    (r'^comments/', include('django.contrib.comments.urls')),
    (r'^ckeditor/', include('ckeditor.urls')),
    (r'^video/', include('video.urls')),
    (r'^admin/', include(admin.site.urls)),
)
