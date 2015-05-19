from django.conf import settings
from django.template import Library

register = Library()

@register.inclusion_tag('touchnet/tags/redirect_tag.html')
def show_redirect_form(form):
    return {'form': form, 'action': settings.TOUCHNET['url']}
