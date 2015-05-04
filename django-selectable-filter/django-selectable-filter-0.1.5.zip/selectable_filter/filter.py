# -*- coding: utf-8 -*-
from django import forms
from django.contrib import admin
from django.db import models
import selectable.forms as selectable


class SelectableBaseForm(forms.Form):
    def __init__(self, request, *args, **kwargs):
        super(SelectableBaseForm, self).__init__(*args, **kwargs)
        self.request = request



class SelectableForm(SelectableBaseForm):

    def __init__(self, *args, **kwargs):
        field_name = kwargs.pop('field_name')
        verbose_field_name = kwargs.pop('verbose_field_name')
        model_lookup = kwargs.pop('model_lookup')
        form_class_selectable = eval(kwargs.pop('form_class_selectable'))
        
        super(SelectableForm, self).__init__(*args, **kwargs)
        self.fields['%s__icontains' % field_name] = forms.CharField(
            label='',
            widget=form_class_selectable(
                lookup_class=model_lookup,
                attrs={'placeholder': verbose_field_name}
            ),
            required=False
        )



class SelectableFilter(admin.filters.FieldListFilter):
    template = 'selectable_filter/filter.html'

    def __init__(self, field, request, params, model, model_admin, field_path):
        package = model._meta.app_label + ".lookups"
        class_lookup = field_path.title() + "Lookup"
        imported_class = getattr(__import__(package, fromlist=[class_lookup]), class_lookup)
        self.model_lookup = imported_class
        try:
            self.related_name = imported_class.field_related_name
        except:
            self.related_name = None

        self.form_class_selectable = imported_class.form_class_selectable
        self.parameter_name = '%s__icontains' % field_path
        self.verbose_field_name = model._meta.get_field(field_path).verbose_name
        super(SelectableFilter, self).__init__(field, request, params, model, model_admin, field_path)
        self.form = self.get_form(request)

    def choices(self, cl):
        return []

    def expected_parameters(self):
        return [self.parameter_name]

    def get_form(self, request):
        return SelectableForm(request, 
                              data=self.used_parameters, 
                              field_name=self.field_path, 
                              verbose_field_name=self.verbose_field_name, 
                              model_lookup=self.model_lookup,
                              form_class_selectable=self.form_class_selectable)

    def queryset(self, request, queryset):
        if self.form.is_valid():
            # get no null params
            filter_params = dict(filter(lambda x: bool(x[1]),
                                        self.form.cleaned_data.items()))

            # filter by upto included
            if filter_params.get(self.parameter_name) is not None:
                lookup_kwarg_upto_value = filter_params.pop(self.parameter_name)
                if self.related_name is None:
                    filter_params['%s__icontains' % self.field_path] = lookup_kwarg_upto_value
                else:
                    filter_params['%s__%s__icontains' % (self.field_path, self.related_name)] = lookup_kwarg_upto_value

            return queryset.filter(**filter_params)
        else:
            return queryset


# register the filters
admin.filters.FieldListFilter.register(
    lambda f: isinstance(f, models.CharField), SelectableFilter)
