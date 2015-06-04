from django.conf.urls import patterns, url
from django.views.generic.base import TemplateView

from jmbo_sitemap import sitemaps, views


urlpatterns = patterns(
    '',

    url(
        r'^sitemap\.xml$',
        views.sitemap,
        {'sitemaps': sitemaps},
        name='sitemap'
    ),

    url(
        r'^sitemap/$',
        views.SitemapHTMLView.as_view(),
        name='html-sitemap'
    ),
)
