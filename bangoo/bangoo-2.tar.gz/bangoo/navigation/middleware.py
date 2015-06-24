from django.http import Http404
from .models import Menu
from .views import menu_dispatcher
from bangoo.admin.views import admin_menu_dispatcher


class MenuResolverMiddleware(object):
    def process_view(self, request, view_func, view_args, view_kwargs):
        """
        Firstly we have to check which view function has to be called. If the view is 'menu_dispatcher' function,
        then find the actual menu according to request.path. If no menu can be found, then raise 404 error.

        If the view isn't 'menu_dispatcher', then it's a 'static' function (defined in project urls.py). 
        > No menu has to be found.
        """

        ## It's a static url, nothing to do.
        if view_func not in (menu_dispatcher, admin_menu_dispatcher):
            return None

        ## If view is admin
        if view_func == admin_menu_dispatcher:
            request.act_menu = Menu.objects.language(request.LANGUAGE_CODE).get(pk=view_kwargs['menu_id'])
            return None

        path = request.path[1:].strip(request.LANGUAGE_CODE)
        parts = path.strip('/').split('/')
        ### Order by menu level desc, mean try to find the actual menu on the most deep level
        menus = Menu.objects.language(request.LANGUAGE_CODE)\
                            .filter(path__startswith='/' + parts[0]).order_by('-level')
        for menu in menus:
            if path.startswith(menu.path):
                request.act_menu = menu
                return None
        raise Http404()