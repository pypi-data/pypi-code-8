# -*- coding: utf-8 -*-

from django.contrib import messages
from django.core.cache import cache
from django.conf import settings
from django.utils.cache import patch_response_headers, get_cache_key
from django.views.decorators.cache import cache_page, never_cache
from django.views.decorators.csrf import csrf_exempt
from django.core.urlresolvers import reverse
from django.http import HttpRequest
from django.core.cache.utils import make_template_fragment_key
from django.db.models import Q


class NeverCacheMixin(object):
    """
    Mixin that never caches views.
    """
    @classmethod
    def as_view(cls, **initkwargs):
        view = super(NeverCacheMixin, cls).as_view(**initkwargs)
        return never_cache(view)


class CSRFExemptMixin(object):
    """
    Mixin that exempts from the CSRF requirements.
    """
    @classmethod
    def as_view(cls, **initkwargs):
        view = super(CSRFExemptMixin, cls).as_view(**initkwargs)
        return csrf_exempt(view)


class CacheMixin(object):
    """
    Mixin that caches the view with the passed cache_timeout value.
    """
    cache_timeout = 60

    @classmethod
    def as_view(cls, **initkwargs):
        view = super(CacheMixin, cls).as_view(**initkwargs)
        return cache_page(cls.cache_timeout)(view)


class CacheControlMixin(object):
    cache_timeout = 60

    def get_cache_timeout(self):
        return self.cache_timeout

    def dispatch(self, *args, **kwargs):
        response = super(CacheControlMixin, self).dispatch(*args, **kwargs)
        patch_response_headers(response, self.get_cache_timeout())
        return response


class ActionMixin(object):
    """
    Used to set a message for the action carried out by the view or form
    http://ferhatelmas.com/blog/2013/05/06/generic-messages-for-users/
    """

    @property
    def action(self):
        msg = "{0} is missing action.".format(self.__class__)
        raise NotImplementedError(msg)

    def form_valid(self, form):
        messages.info(self.request, self.action)
        return super(ActionMixin, self).form_valid(form)


class SearchMixin(object):
    """
    Generic query filter for search
    http://ferhatelmas.com/blog/2013/04/29/generic-search-mixin/
    http://julienphalip.com/post/2825034077/adding-search-to-a-django-site-in-a-snap

    views.py:
    class IndexListView(SlideView, SearchMixin, ListView):
        search_fields = ['titulo', 'texto']

    base.html:
    <form action="" method="GET">
        <input type="text" name="q" />
        <input type="submit" class="btn btn-primary" value="Search" />
    </form>
    """

    def get_queryset(self):
        q = self.request.GET.get('q', None)
        queryset = super(SearchMixin, self).get_queryset()
        if q:
            or_query = None
            for field_name in self.search_fields:
                query = Q(**{"%s__icontains" % field_name: q})
                if or_query is None:
                    or_query = query
                else:
                    or_query = or_query | query
            return queryset.filter(or_query)
        return self.queryset


def expire_view_cache(
    view_name,
    fake_metas={'HTTP_HOST': '', 'SERVER_PORT': 8000},
    args=[],
    namespace=None,
    key_prefix=None,
    method="GET"
):

    """
    This function allows you to invalidate any view-level cache.

    view_name: view function you wish to invalidate or it's named url pattern
    args: any arguments passed to the view function
    namepace: optional, if an application namespace is needed
    key prefix: for the @cache_page decorator for the function (if any)

    http://stackoverflow.com/questions/2268417/expire-a-view-cache-in-django
    added: method to request to get the key generating properly
    """

    # create a fake request object
    request = HttpRequest()
    request.method = method
    request.META = fake_metas
    if settings.USE_I18N:
        request.LANGUAGE_CODE = settings.LANGUAGE_CODE
    # Loookup the request path:
    if namespace:
        view_name = namespace + ":" + view_name
    request.path = reverse(view_name, args=args)
    # get cache key, expire if the cached item exists:
    key = get_cache_key(request, key_prefix=key_prefix)
    if key:
        if cache.get(key):
            cache.set(key, None, 0)
        return True
    return False


def expire_fragment_cache(fragment_name, *variables):

    """
    http://martinbrochhaus.com/caching.html
    """

    cache_key = make_template_fragment_key(
        fragment_name, vary_on=variables)
    cache.delete(cache_key)
