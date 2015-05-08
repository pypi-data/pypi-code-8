# (c) 2011 Bright Interactive Limited. All rights reserved.
# http://www.bright-interactive.com | info@bright-interactive.com

from django import template
import os.path

register = template.Library()

# TODO blomm 03/11/2011: We are missing support for mpeg, flac, wmv and m4v
SUPPORTED_FILE_EXTENSIONS = [
    'pdf', 'doc', 'xls', 'xlsx', 'ppt', 'mp3', 'aac', 'mov', 'mpg', 'avi',
    'wmv', 'mp4', 'm4v', 'ai', 'aiff', 'txt', 'c', 'css', 'dat', 'exe', 'eps',
    'flv', 'html', 'odf', 'ods', 'odt', 'otp', 'ots', 'ott', 'psd', 'py', 'qt',
    'rar', 'rtf', 'sql', 'tgz', 'zip', 'xml', 'tiff', 'tif', 'htm', 'wav'
]


@register.simple_tag(takes_context=False)
def file_icon_class(filename):
    (filename, extension) = os.path.splitext(filename)
    file_extension = extension.lower().lstrip('.')

    if file_extension in SUPPORTED_FILE_EXTENSIONS:
        return file_extension

    return 'unknown'
