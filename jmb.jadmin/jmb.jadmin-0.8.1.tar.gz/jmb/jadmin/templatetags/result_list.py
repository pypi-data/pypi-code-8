
from django.template import Library, loader


register = Library()

@register.filter
def or_required_is_in(value,arg):
    if value in arg or value +":required" in arg:
        return True
    return False

@register.filter
def is_required(value,arg):
    if value +":required" in arg:
        return True
    return False


@register.simple_tag(takes_context=True)
def admin_extra_actions(context, template_name):
    t = loader.get_template(template_name)
    context['action_index'] = context.get('action_index', -1) + 1
    return t.render(context)
