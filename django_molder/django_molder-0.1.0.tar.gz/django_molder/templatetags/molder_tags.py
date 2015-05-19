# coding: utf-8
from django import template
from django.conf import settings
from django.utils import translation
from django.utils.translation import ugettext_lazy as _
from django.utils.text import force_text

from django_molder.renderers import (FieldRenderer, FormRenderer,
                                     MessageRenderer)


register = template.Library()


@register.simple_tag(takes_context=True)
def render_field(context, bound_field, **extra):
    return FieldRenderer(bound_field, **extra).render()


@register.simple_tag(takes_context=True)
def render_form(context, form, **extra):
    return FormRenderer(form, **extra).render()


@register.simple_tag(takes_context=True)
def render_messages(context, **extra):
    request = context['request']
    return MessageRenderer(request, **extra).render()


@register.filter
def iter_choices(bound_field):
    """ Iterator over choices
    """
    field = bound_field.field

    value = bound_field.value()
    if value is not None:
        if hasattr(value, '__iter__'):
            value = set(force_text(v) for v in value)
        else:
            value = [force_text(value)]
    else:
        value = []

    for c_value, c_label in field.widget.choices:
        c_value = force_text(c_value)
        checked = c_value in value
        yield c_value, force_text(c_label), checked
