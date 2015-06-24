from django import template
from django.conf import settings

register = template.Library()

@register.simple_tag(takes_context=True)
def theme_static(context, path):
    return '%sthemes/%s/static/%s' % (settings.STATIC_URL, context.get('ACT_THEME'), path,)