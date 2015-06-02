from django.conf.urls import *

urlpatterns = patterns('leonardo_gallery.views',
    url(r'^(?P<directory_id>[\w\-]+)/$', 'directory_detail_fullscreen', name="directory_detail_standalone"),
)
