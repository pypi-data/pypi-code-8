# encoding: utf-8

from django import template
from django.utils.safestring import mark_safe

from jsonify import compat


register = template.Library()


@register.filter
def jsonify(data):
    return mark_safe(compat.serialize_data(data))
