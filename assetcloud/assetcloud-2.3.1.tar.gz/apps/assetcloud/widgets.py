# (c) 2011 Bright Interactive Limited. All rights reserved.
# http://www.bright-interactive.com | info@bright-interactive.com

from django.forms import widgets
from django.utils.functional import lazy
from django.utils.encoding import force_unicode
from django.utils.html import escape, conditional_escape
from django.utils.safestring import mark_safe
from django.core.urlresolvers import reverse
from sorl.thumbnail.shortcuts import get_thumbnail
import taggit.forms

reverse_lazy = lazy(reverse, str)


class EmailInput(widgets.Input):
    """
    A widget for email inputs.
    We use the HTML5 'email' input, rather than the standard 'text' input.
    """
    input_type = 'email'

    def __init__(self, autocomplete=True, *args, **kwargs):
        if not autocomplete:
            attrs = kwargs.pop('attrs', {})
            attrs['autocomplete'] = 'off'
            kwargs['attrs'] = attrs
        super(EmailInput, self).__init__(*args, **kwargs)


class TagWidget(taggit.forms.TagWidget):
    def __init__(self, attrs=None, *args, **kwargs):
        if attrs is not None:
            attrs = attrs.copy()
        else:
            attrs = {}
        if 'data-autocomplete-url' not in attrs:
            # We have to use reverse_lazy because using reverse would result
            # in a circular dependency between this file and urls.py and
            # cause "The included urlconf urls doesn't have any patterns in
            # it" errors.
            autocomplete_url = reverse_lazy('tag_autocomplete_action')
            attrs['data-autocomplete-url'] = autocomplete_url
        super(TagWidget, self).__init__(attrs=attrs, *args, **kwargs)


class TagSearchWidget(TagWidget):
    input_type = 'search'


class PreviewImageWidget(widgets.ClearableFileInput):
    """
    An ImageField widget that shows the image in the page instead of just
    showing a link to it.
    """

    template_with_initial = u'%(initial)s %(clear_template)s%(input_text)s: %(input)s'

    template_with_clear = u'<label class="checkbox">%(clear)s %(clear_checkbox_label)s</label>'

    def __init__(self, img_class=None, *args, **kwargs):
        """
        img_class: the CSS class to use for the img tag
        """
        super(PreviewImageWidget, self).__init__(*args, **kwargs)
        self.img_class = img_class

    def render(self, name, value, attrs=None):
        substitutions = {
            'initial_text': self.initial_text,
            'input_text': self.input_text,
            'clear_template': '',
            'clear_checkbox_label': self.clear_checkbox_label,
        }
        template = u'%(input)s'
        # We use ClearableFileInput instead of PreviewImageWidget in the
        # super call below to skip ClearableFileInput's implementation of
        # render and call the grandparent class's, because this method was
        # copy/pasted from ClearableFileInput.render() (and then changed).
        substitutions['input'] = super(widgets.ClearableFileInput, self).render(name, value, attrs)

        if value and hasattr(value, "url"):
            thumbnail = get_thumbnail(value, "150x60")
            template = self.template_with_initial
            substitutions['initial'] = (u'<div class="current-image"><a href="%s" target="_blank"><img src="%s" %s/></a></div>'
                                        % (
                                           escape(value.url),
                                           escape(thumbnail.url),
                                           self._img_class_attr(),

                                           )
                                        )
            if not self.is_required:
                checkbox_name = self.clear_checkbox_name(name)
                checkbox_id = self.clear_checkbox_id(checkbox_name)
                substitutions['clear_checkbox_name'] = conditional_escape(checkbox_name)
                substitutions['clear_checkbox_id'] = conditional_escape(checkbox_id)
                substitutions['clear'] = widgets.CheckboxInput().render(checkbox_name, False, attrs={'id': checkbox_id})
                substitutions['clear_template'] = self.template_with_clear % substitutions

        return mark_safe(template % substitutions)

    def _img_class_attr(self):
        if not self.img_class:
            return u''
        else:
            return u'class="%s"' % force_unicode(self.img_class)
