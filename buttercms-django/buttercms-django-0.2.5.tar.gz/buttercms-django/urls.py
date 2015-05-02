from django.conf.urls import patterns, url

from .views import BlogHome, BlogPost, AuthorPage

urlpatterns = [
    url(r'^$', BlogHome.as_view(), name='blog'),
    url(r'^page/(?P<page>\d+)$', BlogHome.as_view(), name='archive'),
    url(r'^author/(?P<author_slug>.*)$', AuthorPage.as_view(), name='blog_author'),
    # This must appear last since it's a catch all
    url(r'^(?P<slug>.*)$', BlogPost.as_view(), name='blog_post'),
]