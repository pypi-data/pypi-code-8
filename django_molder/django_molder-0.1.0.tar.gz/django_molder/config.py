# coding: utf-8
from django import forms
from django.conf import settings


MOLDER_DEFAULT_CLASSES_FOR_WIDGETS = \
    getattr(settings, 'MOLDER_DEFAULT_CLASSES_FOR_WIDGETS', {
        forms.TextInput: 'form-control',
        forms.ClearableFileInput: 'fileinput',
    })

# default class for widgets not listed at `MOLDER_DEFAULT_CLASSES_FOR_WIDGETS`
MOLDER_DEFAULT_CLASSES_FOR_WIDGETS.setdefault(None, '')
