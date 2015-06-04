# -*- coding: utf-8 -*-

from django.conf.urls import patterns, url
from django.contrib.sitemaps import views as sitemaps_views
from django.views.decorators.cache import cache_page
from django.contrib.auth.decorators import login_required
from django.conf import settings as conf

from rblog.feeds import AllFeed, TagFeed
from rblog.views import (BlogIndexView,
                         PostDetailView,
                         PostTempView,
                         PostsWithTag,
                         PostsByDate,
                         AJAXArchive,
                         BlogSitemap,
                         PostLinkAdd,
                         LinkblogIndexView)

sitemaps = {
    'blog': BlogSitemap,
}


########## PRIVACY SETTINGS
def private(myview):
    if conf.RBLOG_PRIVATE:
        return login_required(myview)
    return myview
########## PRIVACY SETTINGS


########## CACHE SETTINGS
def set_cache_view(cview, csetting):
    """
    Returns the view (cached or not, depending on the settings), to properly
    set the url
    """
    if conf.RBLOG_CACHE is True:
        try:
            if csetting != 0:
                return cache_page(csetting)(cview)
            else:
                return cview
        except:
            return cview
    return cview

blog_view = set_cache_view(BlogIndexView.as_view(), conf.RBLOG_CACHE_BLOG)
post_view = set_cache_view(PostDetailView.as_view(), conf.RBLOG_CACHE_POST)
archive_view = set_cache_view(AJAXArchive.as_view(), conf.RBLOG_CACHE_ARCHIVE)
########## CACHE SETTINGS


########## URL SETTINGS
urlpatterns = patterns(
    '',

    url(r'^$',
        private(blog_view),
        name='index'),

    url(r'^linkblog/$',
        private(LinkblogIndexView.as_view()),
        name='linkblog'),

    url(r'^page/(?P<page>\d+)/$',
        private(blog_view),
        name='page'),

    url(r'^(?P<slug>[-\w]+)\.html$',
        private(post_view),
        name='post_detail'),

    url(r'^(?P<slug>[-\w]+)\.tmp$',
        private(PostTempView.as_view()),
        name='post_detail_temp'),

    url(r'^(?P<year>\d{4})/(?P<month>\d{1,2})/$',
        private(PostsByDate.as_view()),
        name='archive'),

    url(r'^(?P<year>\d{4})/(?P<month>\d{1,2})/page/(?P<page>\d+)/$',
        private(PostsByDate.as_view()),
        name='archive_page'),

    url(r'^tag-(?P<tag>[-_A-Za-z0-9]+)/$',
        private(PostsWithTag.as_view()),
        name='with_tag'),

    url(r'^tag-(?P<tag>[-_A-Za-z0-9]+)/page/(?P<page>\d+)/$',
        private(PostsWithTag.as_view()),
        name='with_tag_page'),

    url(r'^tag-(?P<tag>[-_A-Za-z0-9]+)/feed/$',
        private(TagFeed()),
        name='tagfeed'),

    url(r'^tag-(?P<tag>[-_A-Za-z0-9]+)/feed.rss$',
        private(TagFeed()),
        name='tagfeed2'),

    url(r'^feed/$',
        private(AllFeed()),
        name='feed'),

    url(r'^feed.rss$',
        private(AllFeed()),
        name='feed2'),

    url(r'^post/link/add/$',
        private(PostLinkAdd.as_view()),
        name='link_add'),

    url(r'^archive/$',
        private(archive_view),
        name='ajaxarchive'),  # 7 days cache

    url(r'^sitemap\.xml$',
        private(sitemaps_views.sitemap),
        {'sitemaps': sitemaps})
)
########## URL SETTINGS

