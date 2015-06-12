import warnings
from functools import wraps

from django.views.generic import TemplateView
from django.contrib.sitemaps.views import x_robots_tag
from django.contrib.sites.models import get_current_site
from django.core.paginator import EmptyPage, PageNotAnInteger
from django.http import Http404
from django.template.response import TemplateResponse
from django.utils import six

from preferences import preferences


class SitemapHTMLView(TemplateView):
    template_name = "jmbo_sitemap/sitemap.html"

    def get_context_data(self, **kwargs):
        context = super(SitemapHTMLView, self).get_context_data(**kwargs)
        context["content"] = preferences.HTMLSitemap.content
        return context


"""Slight adaptation of default Django sitemaps view passes request to callable
site object"""
@x_robots_tag
def sitemap(request, sitemaps, section=None,
            template_name='sitemap.xml', content_type='application/xml',
            mimetype=None):

    if mimetype:
        warnings.warn("The mimetype keyword argument is deprecated, use "
            "content_type instead", DeprecationWarning, stacklevel=2)
        content_type = mimetype

    req_protocol = 'https' if request.is_secure() else 'http'
    req_site = get_current_site(request)

    if section is not None:
        if section not in sitemaps:
            raise Http404("No sitemap available for section: %r" % section)
        maps = [sitemaps[section]]
    else:
        maps = list(six.itervalues(sitemaps))
    page = request.GET.get("p", 1)

    urls = []
    for site in maps:
        try:
            if callable(site):
                try:
                    site = site(request)
                except TypeError:
                    site = site()
            urls.extend(site.get_urls(page=page, site=req_site,
                                      protocol=req_protocol))
        except EmptyPage:
            raise Http404("Page %s empty" % page)
        except PageNotAnInteger:
            raise Http404("No page '%s'" % page)
    # Google will not accept a sitemap with no urls. In such a case link back
    # to the site.
    if not urls:
        urls = [{'location': '%s://%s' % (req_protocol, req_site.domain)}]
    return TemplateResponse(request, template_name, {'urlset': urls},
                            content_type=content_type)
