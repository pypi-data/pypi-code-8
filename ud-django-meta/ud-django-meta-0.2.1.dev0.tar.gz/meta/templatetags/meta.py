from __future__ import absolute_import, unicode_literals

from django import template
from django.utils.html import escape

register = template.Library()


@register.simple_tag
def generic_prop(namespace, name, value):
    """
    Generic property setter that allows to create custom namespaced meta
    """
    return '<meta property="%s:%s" content="%s">' % (escape(namespace), escape(name), escape(value))


@register.simple_tag
def og_prop(name, value):
    return '<meta property="og:%s" content="%s">' % (escape(name), escape(value))


@register.simple_tag
def twitter_prop(name, value):
    return '<meta name="twitter:%s" content="%s">' % (escape(name), escape(value))


@register.simple_tag
def googleplus_prop(name, value):
    return '<meta itemprop="%s" content="%s">' % (escape(name), escape(value))


@register.simple_tag
def googleplus_html_scope(value):
    """
    This is meant to be used as attribute to html / body or other tags to
    define schema.org type
    """
    return ' itemscope itemtype="http://schema.org/%s" ' % escape(value)


@register.simple_tag
def meta(name, value):
    return '<meta name="%s" content="%s">' % (escape(name), escape(value))

@register.simple_tag
def custom_meta(name_key, name_value, content):
    return '<meta %s="%s" content="%s">' % (escape(name_key), escape(name_value), escape(content))

@register.simple_tag
def meta_list(name, lst):
    try:
        return '<meta name="%s" content="%s">' % (escape(name), escape(', '.join(lst)))
    except:
        return ''

@register.simple_tag
def meta_extras(extra_props):
    return ' '.join([meta(name, extra_props[name]) if extra_props[name] else ''
                     for name in extra_props])

@register.simple_tag
def custom_meta_extras(extra_custom_props):
    return ' '.join([custom_meta(name_key, name_value, content) if content else ''
                     for name_key, name_value, content in extra_custom_props])
