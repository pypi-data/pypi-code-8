import json

from django.contrib.auth.decorators import permission_required
from django.db import transaction, IntegrityError
from django.http import HttpResponse, HttpResponseBadRequest
from django.shortcuts import render, get_object_or_404
from django.utils.translation import ugettext_lazy as _
from django.views.generic import View

from bangoo.content.models import Content
from bangoo.decorators import class_view_decorator
from bangoo.navigation.menu.forms import MenuOrderForm, MenuRenameForm, MenuCreateForm
from bangoo.navigation.models import Menu

from .signals import menu_changed
from .utils import create_path


@permission_required('menu.add_menu')
def menu(request, template_name='navigation/menu/menu.html'):
    return render(request, template_name, {'nodes': Menu.objects.all(), 'form': MenuCreateForm()})


@class_view_decorator(permission_required('menu.add_menu'))
class ReorderMenuView(View):
    def post(self, request, *args, **kwargs):
        form = MenuOrderForm(request.POST)
        if form.is_valid():
            try:
                with transaction.atomic():
                    changed_paths = []

                    method = form.cleaned_data['method']
                    target_menu = form.cleaned_data['target']
                    source_menu = form.cleaned_data['source']

                    if method == 'move':
                        source_menu_parent = source_menu.parent
                        source_menu.move_to(target_menu, position='left')
                        source_menu.save()

                        menu_changed.send(sender=self.__class__,
                                          menu=source_menu,
                                          old_parent=source_menu_parent,
                                          new_parent=target_menu.parent)

                    if method == 'insert':
                        source_menu_parent = source_menu.parent
                        source_menu.move_to(target_menu)
                        source_menu.save()

                        menu_changed.send(sender=self.__class__,
                                          menu=source_menu,
                                          old_parent=source_menu_parent,
                                          new_parent=target_menu)

                    if method in {'move', 'insert'}:
                        for descendant in source_menu.get_descendants(include_self=True):
                            old_path = descendant.path

                            descendant.path = create_path(descendant)
                            descendant.save()

                            if descendant.plugin == 'bangoo.content':
                                content = Content.objects.language(descendant.language_code).filter(url=old_path).first()
                                content.url = descendant.path
                                content.save()

                            changed_paths.append({
                                'menu_id': descendant.id,
                                'path': descendant.path
                            })
                        return HttpResponse(json.dumps(changed_paths), content_type='application/json')
            except IntegrityError:
                return HttpResponseBadRequest(_("Failed to move the menu item because there is already one "
                                                "with the same name under the destination path."))
        else:
            reason = {
                'status': 'error',
                'reasons': dict([(k, form.error_class.as_text(v)) for k, v in list(form.errors.items())])
            }
            return HttpResponse(json.dumps(reason), content_type='application/json')


@class_view_decorator(permission_required('menu.add_menu'))
class RenameMenuView(View):
    def post(self, request, *args, **kwargs):
        menu_id = kwargs.pop('menu_id', None)
        menu = get_object_or_404(Menu, pk=menu_id)
        form = MenuRenameForm(request.POST, menu=menu)

        if form.is_valid():
            with transaction.atomic():
                changed_paths = []

                menu.title = form.cleaned_data['title']
                menu.path = create_path(menu)
                menu.save()

                changed_paths.append({
                    'menu_id': menu.id,
                    'path': menu.path
                })

                for descendant in menu.get_descendants():
                    descendant.path = create_path(descendant)
                    descendant.save()

                    changed_paths.append({
                        'menu_id': descendant.id,
                        'path': descendant.path
                    })

                return HttpResponse(json.dumps(changed_paths), content_type='application/json')
        else:
            reason = {
                'status': 'error',
                'menu_id': menu_id,
                'reasons': dict([(k, form.error_class.as_text(v)) for k, v in list(form.errors.items())])
            }
            return HttpResponse(json.dumps(reason), content_type='application/json')
