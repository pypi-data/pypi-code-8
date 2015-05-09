from django.conf.urls import *
from django.views.defaults import shortcut

from nano.comments.models import *

comment_dict = {}


urlpatterns = patterns('',
    url(r'^$',         views.list_comments, comment_dict, name='comments-list-comments'),
    url(r'^post$',     views.post_comment, name='comments-post-comment'),
)

urlpatterns += patterns('',
    url(r'^cr/(\d+)/(.+)/$', shortcut, name='comments-url-redirect'),
)

