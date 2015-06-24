from django.core.urlresolvers import resolve
from bangoo.navigation.utils import get_urlconf


def menu_dispatcher(request):
    path = request.path[1:].strip(request.LANGUAGE_CODE)
    func, args, kwargs = resolve(path[len(request.act_menu.path) - 1:], urlconf=get_urlconf(request.act_menu.plugin))
    return func(request, *args, **kwargs)