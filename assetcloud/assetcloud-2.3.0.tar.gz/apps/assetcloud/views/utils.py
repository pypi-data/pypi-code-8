__all__ = [
    'view_is_public'
]

from django.conf import settings
import re


def view_is_public(request, view_func, view_args, view_kwargs):
    return _is_login(request) \
        or _is_decorated_with_public(view_func) \
        or _in_public_urls(request)


def _is_login(request):
    return request.path == settings.LOGIN_URL


def _is_decorated_with_public(view_func):
    return getattr(view_func, 'public', False)


def _in_public_urls(request):
    path = request.path

    # for consistency with Django url resolution - patterns don't start
    # with '/' for some reason even though request.path does
    if path.startswith('/'):
        path = path[1:]

    for pattern in getattr(settings, 'PUBLIC_URLS', ()):
        if re.search(pattern, path):
            return True
    return False
