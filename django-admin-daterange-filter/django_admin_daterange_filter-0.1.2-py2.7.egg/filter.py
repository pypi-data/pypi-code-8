from django.contrib import admin
from django import forms
import datetime
from django.forms.widgets import TextInput
from django.utils.translation import ugettext as _
from django.conf import settings

class DateInput(TextInput):
    def render(self, name, value, attrs=None):
        rs = super(DateInput,self).render(name,value,attrs)
        js = '<script>\
        django.jQuery( "#%s" ).datepicker({\
            changeMonth: true,\
            showButtonPanel: true,\
            numberOfMonths: 3,\
        });\
        </script>' % attrs['id']
        return rs + js
    
class DateRangeForm(forms.Form):
    def __init__(self, *args, **kwargs):
        field_name = kwargs.pop('field_name')
        super(DateRangeForm, self).__init__(*args, **kwargs)
        self.fields['%s__gte' % field_name] = forms.DateField(
            label='',
            widget=DateInput(
                attrs={'placeholder': _('From date')}
            ),
            localize=True,
            required=False
        )

        self.fields['%s__lte' % field_name] = forms.DateField(
            label='',
            widget=DateInput(
                attrs={'placeholder': _('To date')}
            ),
            localize=True,
            required=False,
        )
    @property
    def media(self):
        js = [
              'admin_daterange_filter/ui/jquery.ui.core.js',
              'admin_daterange_filter/ui/jquery.ui.datepicker.js',
              ]
        if settings.LANGUAGE_CODE!='en_us':
            js.append('admin_daterange_filter/ui/i18n/jquery.ui.datepicker-%s.js' % settings.LANGUAGE_CODE)
        return forms.Media(
            js =js,
            css = {'all':('admin_daterange_filter/themes/base/jquery.ui.all.css',)},
        )

class DateRangeFilter(admin.filters.FieldListFilter):
    template = 'admin_daterange_filter/filter.html'

    def __init__(self, field, request, params, model, model_admin, field_path):
        self.lookup_kwarg_since = '%s__gte' % field_path
        self.lookup_kwarg_upto = '%s__lte' % field_path
        super(DateRangeFilter, self).__init__(
            field, request, params, model, model_admin, field_path)
        self.form = self.get_form(request)

    def choices(self, cl):
        return []

    def expected_parameters(self):
        return [self.lookup_kwarg_since, self.lookup_kwarg_upto]

    def get_form(self, request):
        return DateRangeForm(data=self.used_parameters,
                             field_name=self.field_path)

    def queryset(self, request, queryset):
        if self.form.is_valid():
            # get no null params
            filter_params = dict(filter(lambda x: bool(x[1]),
                                        self.form.cleaned_data.items()))

            # filter by upto included
            if filter_params.get(self.lookup_kwarg_upto) is not None:
                lookup_kwarg_upto_value = filter_params.pop(self.lookup_kwarg_upto)
                filter_params['%s__lt' % self.field_path] = lookup_kwarg_upto_value + datetime.timedelta(days=1)

            return queryset.filter(**filter_params)
        else:
            return queryset
