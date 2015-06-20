from django import template

from horizon.utils import units

register = template.Library()


@register.filter
def normalize(value, unit=None):
    """Converts the value so that it belongs to some expected range.
    Returns the new value and new unit.
    E.g:
    >>> normalize(1024, 'KB')
    (1, 'MB')
    >>> normalize(90, 'min')
    (1.5, 'hr')
    >>> normalize(1.0, 'object')
    (1, 'object')
    """
    return units.normalize(value, unit)
