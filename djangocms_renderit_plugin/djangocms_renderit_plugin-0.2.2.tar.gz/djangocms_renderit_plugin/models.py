from __future__ import unicode_literals
from django.db import models
from django.conf import settings
from cms.models import CMSPlugin
from django.template import Template

TEMPLATE = (
    '{% load cms_tags #ADDITIONAL_LIBRARIES# %}'
    '#OUTPUT#')


ERROR_TEMPLATE = ('{output_wrap_start}'
                  '<div style="'
                  'max-height: 300px; '
                  'max-width: 100%; '
                  'overflow: auto; '
                  'padding: 5px; '
                  'background: #eee;"'
                  '>'
                  '    <span style="color: red;">{message}</span>'
                  '    {output_inner}'
                  '</div>'
                  '{output_wrap_end}')

ERROR_OUTPUT_TEMPLATE = '<div style="border: 1px dotted red; padding: 0;">{}</div>'


class RenderitCMSPlugin(CMSPlugin):
    tag_libraries = models.CharField(max_length=255, null=False, blank=True, default='',
                                     help_text='Custom tag libraries, space-separated')

    def _get_tag_libraries(self):
        try:
            libraries = ' '.join(map(str, settings.CMS_RENDERIT_TAG_LIBRARIES))
        except AttributeError:
            libraries = ''
        if self.tag_libraries:
            libraries = ' '.join((libraries, self.tag_libraries))
        return libraries

    def render_plugin(self, context=None, placeholder=None, admin=False, processors=None):
        output = super(RenderitCMSPlugin, self).render_plugin(context, placeholder, admin, processors)

        template_str = TEMPLATE.replace(
            '#OUTPUT#', output
        ).replace(
            '#ADDITIONAL_LIBRARIES#', self._get_tag_libraries()
        )
        try:
            return Template(template_str).render(context)
        except Exception as e:
            return self.render_exception(e, output)

    def render_exception(self, e, output=None):
        """ Render error message, preserving clickable wrappers
            for easy access to parent "renderit" plugin.
        """
        expected_start = '<div class="cms_plugin cms_plugin-{}">'.format(self.id)
        expected_end = '</div>'
        if (output[:len(expected_start)] == expected_start
                and output[-len(expected_end):] == expected_end):
            output_inner = output[len(expected_start):-len(expected_end)]
            output_wrap_start = expected_start
            output_wrap_end = expected_end
        else:
            # we are most likely not in edit mode, so no clickable div wrapper
            output_inner = output
            output_wrap_start = ''
            output_wrap_end = ''
        return ERROR_TEMPLATE.format(
            message=str(e),
            output_inner='' if not output_inner else ERROR_OUTPUT_TEMPLATE.format(output),
            output_wrap_start=output_wrap_start,
            output_wrap_end=output_wrap_end,
        )
