from django import template


register = template.Library()


@register.simple_tag
def sample():
    return 'HERE BE DA SIMPLE TAG!'
