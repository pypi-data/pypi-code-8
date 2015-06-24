from django.conf.urls import patterns, include, url

from jmbo.urls import v1_api
from jmbo.views import ObjectDetail

from video.api import VideoResource


v1_api.register(VideoResource())

urlpatterns = patterns(
    '',
    url(
        r'^(?P<category_slug>[\w-]+)/(?P<slug>[\w-]+)/$',
        ObjectDetail.as_view(),
        name='video_categorized_object_detail'
    ),
    url(
        r'^(?P<slug>[\w-]+)/$',
        ObjectDetail.as_view(),
        name='video_object_detail'
    ),
)
