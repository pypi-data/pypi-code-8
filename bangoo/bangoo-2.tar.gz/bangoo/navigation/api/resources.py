# coding: utf-8

import json

from restify.authorization import DjangoPermissions
from restify.http import status
from restify.http.response import ApiResponse
from restify.resource import ModelResource

from bangoo.navigation.menu.forms import MenuCreateForm
from bangoo.navigation.models import Menu


class MenuResource(ModelResource):
    class Meta:
        resource_name = 'menu-api'
        authorization = DjangoPermissions(get='navigation.add_menu', post='navigation.add_menu')

    def common(self, request, menu_id):
        post = request.body.decode()
        self.form = MenuCreateForm(json.loads(post) if post != '' else None)

    def get(self, request, menu_id):
        return ApiResponse(self.form)

    def post(self, request, menu_id):
        if self.form.is_valid():
            data = self.form.cleaned_data

            plugin = data['plugin']
            titles = {}

            add_menu_kwargs = {}
            if data['parent']:
                add_menu_kwargs['parent'] = data['parent']

            for k, v in data.items():
                if k in self.form.language_fields:
                    code = self.form.language_fields[k]
                    titles[code] = v

            menu = Menu.handler.add_menu(titles=titles, plugin=plugin, user=request.user, **add_menu_kwargs)
            # TODO: We might return with too much information
            return ApiResponse(menu)
        return ApiResponse(self.form, status_code=status.HTTP_400_BAD_REQUEST)
