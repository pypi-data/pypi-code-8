from django.conf.urls import url

from tastypie.resources import ModelResource
from jmbo.api import ModelBaseResource

from video.models import Video


class VideoResource(ModelBaseResource):

    class Meta:
        queryset = Video.permitted.all()
        resource_name = 'video'
