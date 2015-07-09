from django import template
from django_image import settings

register = template.Library()

def split_kwargs(kwargs):
    """Split out kwargs into options and attributes"""
    options = {k: v for k, v in kwargs.items() if not k.startswith('_')}
    attributes = {k.lstrip('_'): v for k, v in kwargs.items() if k.startswith('_')}
    return (options, attributes)

@register.simple_tag(takes_context=True)
def image(context, f, **kwargs):
    options, attributes = split_kwargs(kwargs)
    return settings.IMAGES_BACKEND.get_html(f, options, attributes)

@register.assignment_tag(takes_context=True)
def imageas(context, f, **kwargs):
    options, attributes = split_kwargs(kwargs)
    return image(context, f, **kwargs)

@register.simple_tag(takes_context=True)
def imageurl(context, f, **kwargs):
    options, attributes = split_kwargs(kwargs)
    return settings.IMAGES_BACKEND.get_url(f, options)

@register.assignment_tag(takes_context=True)
def imageurlas(context, f, **kwargs):
    return imageurl(context, f, **kwargs)
