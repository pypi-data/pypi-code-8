#coding: utf-8
from django.core.urlresolvers import reverse
from django.core.exceptions import ImproperlyConfigured

# 3rd party
from vanilla import CreateView, DeleteView, ListView, UpdateView
import floppyforms.__future__ as forms

model_forms = forms.models


class CrudUrlMap(object):

    def __init__(self, view):
        namespace = 'frontadmin'
        self.template = '{}:{}.{}.{{}}'.format(
            namespace,
            view.model._meta.app_label,
            view.model._meta.model_name
            )

    @property
    def list(self):
        return self.template.format('list')

    @property
    def create(self):
        return self.template.format('create')

    @property
    def update(self):
        return self.template.format('update')

    @property
    def delete(self):
        return self.template.format('delete')


class Fieldset(object):

    def __init__(self, **kwargs):
        self.id = kwargs.get('id')
        self.legend = kwargs.get('legend')
        self.fields = kwargs.get('fields')

    @staticmethod
    def flatten(fields):
        """Returns a list which is a single level of flattening of the
        original list."""
        flat = []
        for field in fields:
            if isinstance(field, (list, tuple)):
                flat.extend(field)
            else:
                flat.append(field)
        return flat

    def get_flattened_fields(self):
        return self.flatten(self.fields)


class AdminUtilsMixin(object):

    @property
    def urls(self):
        if not hasattr(self, '_urls'):
            self._urls = CrudUrlMap(self)
        return self._urls


class AdminEditMixin(AdminUtilsMixin):

    def get_fields(self):
        field_names = getattr(self, 'fields', None)

        if not field_names:
            field_names = []
            for fieldset in self.fieldsets:
                field_names.extend(
                    fieldset.get_flattened_fields()
                    )
        return field_names or None

    def get_fieldsets(self, request, obj=None):
        """
        Hook for specifying fieldsets.
        """
        if self.fieldsets:
            return self.fieldsets
        return [(None, {'fields': self.get_fields(request, obj)})]

    def get_form_class(self):
        """
        Returns the form class to use in this view.
        """
        if self.form_class is not None:
            return self.form_class

        fields = self.get_fields()

        if self.model is not None and fields is not None:
            return model_forms.modelform_factory(
                self.model,
                fields=self.get_fields()
                )

        msg = "'%s' must either define 'form_class' or both 'model' and " \
              "'fields', or override 'get_form_class()'"
        raise ImproperlyConfigured(msg % self.__class__.__name__)


class AdminListView(AdminUtilsMixin, ListView):
    pass


class AdminUpdateView(AdminEditMixin, UpdateView):

    template_name = 'frontadmin/update.html'

    def get_success_url(self):
        return reverse(self.urls.list)


class AdminCreateView(AdminEditMixin, CreateView):

    template_name = 'frontadmin/create.html'

    def get_success_url(self):
        return reverse(self.urls.list)
