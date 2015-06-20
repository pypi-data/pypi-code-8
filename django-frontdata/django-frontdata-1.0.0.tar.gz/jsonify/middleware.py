# encoding: utf-8

import re

from django.core.exceptions import ImproperlyConfigured
from django.conf import settings
from django.template.loader import render_to_string
from django.utils.encoding import force_text

from jsonify import api


_HTML_TYPES = ('text/html', 'application/xhtml+xml')


class JsonifyMiddleware(object):
    def process_response(self, request, response):
        if self.is_should_inject(request):
            if self.is_can_inject(response):
                self.inject_data(api.get_frontdata(request), response)
            else:
                raise ImproperlyConfigured('Injecting is impossible')
        return response

    def is_should_inject(self, request):
        if not api.has_frontdata(request):
            return False
        return bool(api.get_frontdata(request))

    def is_can_inject(self, response):
        """
        https://github.com/django-debug-toolbar/django-debug-toolbar/blob/master/debug_toolbar/middleware.py#L105
        """
        content_encoding = response.get('Content-Encoding', '')
        content_type = response.get('Content-Type', '').split(';')[0]
        if any((getattr(response, 'streaming', False),
                'gzip' in content_encoding,
                content_type not in _HTML_TYPES)):
            return False
        return True

    def inject_data(self, data, response):
        """
        https://github.com/django-debug-toolbar/django-debug-toolbar/blob/master/debug_toolbar/middleware.py#L117
        """
        content = force_text(response.content, encoding=settings.DEFAULT_CHARSET)
        insert_before = '</body>'
        try:                    # Python >= 2.7
            pattern = re.escape(insert_before)
            bits = re.split(pattern, content, flags=re.IGNORECASE)
        except TypeError:       # Python < 2.7
            pattern = '(.+?)(%s|$)' % re.escape(insert_before)
            matches = re.findall(pattern, content, flags=re.DOTALL | re.IGNORECASE)
            bits = [m[0] for m in matches if m[1] == insert_before]
            # When the body ends with a newline, there's two trailing groups.
            bits.append(''.join(m[0] for m in matches if m[1] == ''))
        if len(bits) > 1:
            bits[-2] += self.render_data(data)
            response.content = insert_before.join(bits)
            if response.get('Content-Length', None):
                response['Content-Length'] = len(response.content)
        return response

    def render_data(self, data):
        return render_to_string('jsonify/inject.html', {
            'data': dict(data),
        })
