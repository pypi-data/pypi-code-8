# -*- coding: utf-8 -*-
import datetime

from django.conf import settings
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.admin.views.main import ALL_VAR, ORDER_VAR, ORDER_TYPE_VAR, PAGE_VAR, SEARCH_VAR
from django.contrib.admin.views.main import TO_FIELD_VAR, IS_POPUP_VAR, ERROR_FLAG
from django.db import models
from django.utils.translation import ugettext as _
from django.utils.encoding import smart_unicode, smart_str, force_unicode
from django.template import Library
from django.utils.http import urlencode
from django.utils.safestring import mark_safe
from django.forms.forms import BoundField

register = Library()

@register.inclusion_tag("filters/advanced_search_form.html", takes_context = True)
def advanced_search_form(context, cl):

    request = context['request']    
    search_form = None
    display_fields = None
    display_fields_new = []

    if hasattr(cl.model_admin, 'search_filterset'):
        search_form = cl.model_admin.search_filterset.form
        display_fields = cl.model_admin.search_filterset.Meta.fields

    return {
        'search_form' : search_form,
        'search_or_filters': (getattr(cl, 'search_fields', None) or cl.has_filters),
#        'search_or_filters': (hasattr(cl, 'search_fields') or cl.has_filters),
        'display_fields' : display_fields
    }

@register.simple_tag
def search_form_row(search_form, name):
    name2 = "".join(name.split(":")[:-1]) if ":" in name else name  
    field = search_form.fields[name2]
    bf = BoundField(search_form, field, name2)
    return mark_safe("<td>%s</td><td>%s</td>" % (_(bf.label), bf))

@register.simple_tag
def get_query_string_param(cl):
    v = (ALL_VAR, ORDER_VAR, ORDER_TYPE_VAR, PAGE_VAR, SEARCH_VAR, TO_FIELD_VAR, IS_POPUP_VAR)
    params = cl.params
    new_params = cl.params.copy()
    for p in params:
        if p not in v:
            del new_params[p]
    qs = urlencode(new_params)
    return qs

@register.inclusion_tag('filters/search_form.html')
def jsearch_form(cl):
    """
    Displays a search form for searching the list.
    """
    return {
        # the search toolbar is shown if some filter is available
        'show_filters' : (getattr(cl, 'search_fields', None) or 
                          hasattr(cl.model_admin, 'search_form') or
                          cl.has_filters) ,
        'advanced_search' : hasattr(cl.model_admin, 'search_form'),
        'cl': cl,
        'show_result_count': cl.result_count != cl.full_result_count,
        'search_var': SEARCH_VAR
    }
