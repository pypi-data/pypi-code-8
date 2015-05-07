from django import template

register = template.Library()


@register.simple_tag(takes_context=True)
def nav_classes(context, section):
    """
    Return css classes for a navigation link.

    The section's name should always be applied as a class.
    If the section is selected then the 'active' class should be applied.
    """
    if section == context.get('section', None):
        return section + " active"
    return section


@register.simple_tag(takes_context=True)
def nav_subsection_classes(context, subsection):
    """
    Return css classes for a navigation link to a subsection.

    If the subsection is selected then the 'active' class should be applied.
    """
    if subsection == context.get('subsection', None):
        return "active"
    return ""
