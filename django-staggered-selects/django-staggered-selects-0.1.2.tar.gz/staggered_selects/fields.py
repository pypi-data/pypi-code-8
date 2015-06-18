# Imports from django
from django.db import models
from django import forms


# Imports from staggered-select
from staggered_selects.widgets import StaggeredSelectWidget


class StaggeredSelectFormField(forms.CharField):
    widget = StaggeredSelectWidget


class StaggeredSelectField(models.CharField):
    def __init__(self, *args, **kwargs):
        self.watched_field = kwargs.pop('watched_field', '')
        self.get_choices = kwargs.pop('get_choices_function', '')

        super(StaggeredSelectField, self).__init__(
            *args,
            **kwargs
        )

    def formfield(self, **kwargs):
        defaults = {}
        defaults.update(kwargs)

        defaults['widget'] = StaggeredSelectWidget
        defaults['form_class'] = StaggeredSelectFormField

        form_field = super(StaggeredSelectField, self).formfield(**defaults)

        form_field.widget.attrs['watched_field'] = self.watched_field
        form_field.widget.attrs['get_choices_function'] = self.get_choices

        return form_field

