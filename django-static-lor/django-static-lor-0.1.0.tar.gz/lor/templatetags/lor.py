from __future__ import absolute_import

import os
import warnings
from django import template
from django.conf import settings as se
from lor.settings import FILES_URLS, USE_LOCAL_URLS

register = template.Library()


@register.simple_tag
def lor_url(file_name):
    if file_name not in FILES_URLS:
        warnings.warn("'%s' not defined." % file_name)
        return ''
    file_matches = FILES_URLS[file_name]
    if USE_LOCAL_URLS:
        if not file_matches[0]:
            return ''
        return os.path.join(se.STATIC_URL, file_matches[0])
    elif len(file_matches) > 1 and file_matches[1]:
        return file_matches[1]
    else:
        warnings.warn("No local '%s' defined.")
        return ''
