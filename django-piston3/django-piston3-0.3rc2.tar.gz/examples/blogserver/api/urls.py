from django.conf.urls import *
from piston3.resource import Resource
from piston3.authentication import HttpBasicAuthentication
from piston3.doc import documentation_view

from blogserver.api.handlers import BlogpostHandler

auth = HttpBasicAuthentication(realm='My sample API')

blogposts = Resource(handler=BlogpostHandler, authentication=auth)

urlpatterns = patterns('',
    url(r'^posts/$', blogposts),
    url(r'^posts/(?P<emitter_format>.+)/$', blogposts),
    url(r'^posts\.(?P<emitter_format>.+)', blogposts, name='blogposts'),

    # automated documentation
    url(r'^$', documentation_view),
)
