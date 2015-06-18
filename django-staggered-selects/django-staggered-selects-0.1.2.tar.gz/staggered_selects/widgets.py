# Imports from django
from django.forms import widgets
from django.utils.safestring import mark_safe


class StaggeredSelectWidget(widgets.TextInput):
    '''
    '''
    class Media:
        css = {
            'all': ('staggered_select/css/staggered.css',),
        }
        js = (
            'staggered_select/js/staggered.js',
        )

    def render(self, name, value, attrs=None):
        html = super(StaggeredSelectWidget, self).render(
            name,
            value,
            attrs
        )

        html = [
            '<div class="sselect-message">Choose a <span class="watched-verbose">value</span> to see options.</div>',
            '<select class="staggered-select">',
            '</select>',
            '%s' % html,
        ]

        return mark_safe(''.join(html))
