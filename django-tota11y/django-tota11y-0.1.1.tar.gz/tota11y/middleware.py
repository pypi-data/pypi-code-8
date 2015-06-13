import re

from django.conf import settings
from django.utils.encoding import force_text
from django.template.loader import render_to_string


_HTML_TYPES = ('text/html', 'application/xhtml+xml')


class Tota11yMiddleware(object):

    def process_response(self, request, response):
        content_encoding = response.get('Content-Encoding', '')
        content_type = response.get('Content-Type', '').split(';')[0]
        if any((getattr(response, 'streaming', False),
                'gzip' in content_encoding,
                content_type not in _HTML_TYPES)):
            return response

        content = force_text(response.content, encoding=settings.DEFAULT_CHARSET)
        insert_before = '</body>'
        try:
            pattern = re.escape(insert_before)
            bits = re.split(pattern, content, flags=re.IGNORECASE)
        except:
            pattern = '(.+?)(%s|$)' % re.escape(insert_before)
            matches = re.findall(pattern, content, flags=re.DOTALL | re.IGNORECASE)
            bits = [m[0] for m in matches if m[1] == insert_before]
            bits.append(''.join(m[0] for m in matches if m[1] == ''))
        if len(bits) > 1:
            bits[-2] += render_to_string('tota11y/base.html')
            response.content = insert_before.join(bits)
            if response.get('Content-Length', None):
                response['Content-Length'] = len(response.content)
        return response
