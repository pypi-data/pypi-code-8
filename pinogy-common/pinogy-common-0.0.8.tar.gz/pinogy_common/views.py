# -*- coding: utf-8 -*-

from __future__ import unicode_literals

from django.http import (
    Http404,
    HttpResponseRedirect,
    HttpResponsePermanentRedirect,
)

from menus.utils import set_language_changer
from parler.views import ViewUrlMixin


class CMSLanguageChangerMixin(object):
    """Just adds support for the language changer in CMS."""
    def get(self, request, *args, **kwargs):
        response = super(CMSLanguageChangerMixin, self).get(
            request, *args, **kwargs)
        # We're assured to have self.object set after the call to super.
        set_language_changer(request, self.object.get_absolute_url)
        return response


class CanonicalUrlMixin(ViewUrlMixin):
    """
    Provides configurable control over how non-canonical URLs to views are
    handled. A view can specify by setting 'non_canonical_url_response_type' to
    one of 200, 301, 302 or 404. By default, handling will be to temporarily
    redirect to the canonical URL.
    """
    non_canonical_url_response_type = 302

    def get_non_canonical_url_response_type(self):
        response_type = getattr(self, "non_canonical_url_response_type", None)
        if response_type and response_type in [200, 301, 302, 404]:
            return response_type
        else:
            return 302

    def get(self, request, *args, **kwargs):
        """
        On GET, if the URL used is not the correct one, handle according to
        preferences by either:
            Allowing (200),
            Temprarily redirecting (302),
            Permanently redirecting (301) or
            Failing (404).
        """
        if not hasattr(self, 'object'):
            self.object = self.get_object()
        url = self.get_view_url()
        response_type = self.get_non_canonical_url_response_type()
        if (response_type == 200 or request.path == url):
            return super(CanonicalUrlMixin, self).get(
                request, *args, **kwargs)
        if response_type == 302:
            return HttpResponseRedirect(url)
        elif response_type == 301:
            return HttpResponsePermanentRedirect(url)
        else:
            raise Http404('This is not the canonical uri of this object.')
