from PIL import Image, ImageDraw
from django.contrib.webdesign import lorem_ipsum
import StringIO
import curses.ascii
import macpath
import ntpath
import os
import random
import string
import sys
import unicodedata


def _want(uc):
    cat = unicodedata.category(uc)
    return (cat[0] in 'LMNPSZ')

LOTS_OF_UNICODE_CHARS = ''.join(
    unichr(char)
    for char in xrange(sys.maxunicode + 1)
    if _want(unichr(char)))

# Printable chars, not including the control characters.
REGULAR_CHARS = ''.join(char for char in string.printable
                        if not curses.ascii.iscntrl(char))

REGULAR_CHARS_EXCLUDING_DOT_SPACE_AND_SEP = REGULAR_CHARS.replace('.', '').replace(' ', '')
for sep in [os.sep, os.altsep, macpath.sep, macpath.altsep, ntpath.sep, ntpath.altsep]:
    if sep:
        for char in sep:
            REGULAR_CHARS_EXCLUDING_DOT_SPACE_AND_SEP = REGULAR_CHARS_EXCLUDING_DOT_SPACE_AND_SEP.replace(char, '')


def random_domain(length=8, suffix='.com'):
    """
    A random domain name.
    """
    chars = string.lowercase + string.digits + '-'
    domain = None
    while domain is None or domain.startswith('-') or domain.endswith('-'):
        domain = random_unicode(length, chars)
    return domain + suffix


def random_email_user(length=8):
    """
    A random email local part.
    """
    chars = string.letters + string.digits + "!#$%&'*+-/=?^_`{|}~."
    local = None
    while (local is None or local.startswith('.') or local.endswith('.')
           or '..' in local):
        local = random_unicode(length, chars)
    return local


def random_email(length=8):
    """
    A random email address.

    See: http://stackoverflow.com/questions/2049502/what-characters-are-allowed-in-email-address
    """
    return (random_email_user(length) + '@' + random_domain()).lower()


def random_alphanumeric(length=8):
    """
    A random string of uppercase, lowercase, and digits.
    """
    chars = string.letters + string.digits
    return random_unicode(length, chars)


def random_filename(length=8, suffix='.bin'):
    """
    A random string of any regular printable char, with a suffix.
    """
    return random_unicode(length, REGULAR_CHARS_EXCLUDING_DOT_SPACE_AND_SEP) + suffix


def random_image_file(filename=None, suffix='.png', width=None, height=None):
    """
    Return a random image file-like object.
    """
    if filename is not None:
        basename, suffix = os.path.splitext(filename)

    if width is None:
        width = random.randint(100, 1000)
    if height is None:
        height = random.randint(100, 1000)

    ink = "red", "blue", "green", "yellow", "black"
    image = Image.new("RGB", (width, height), random.choice(ink))
    draw = ImageDraw.Draw(image)
    for rect in range(random.randint(1, 10)):
        x1 = random.randint(0, width)
        x2 = random.randint(0, width)
        y1 = random.randint(0, height)
        y2 = random.randint(0, height)
        coords = (min(x1, x2), min(y1, y2), max(x1, x2), max(y1, y2))
        draw.rectangle(coords, fill=random.choice(ink))

    output = StringIO.StringIO()
    image.save(output, format=suffix.lstrip('.'))
    content = output.getvalue()
    output.close()
    return random_file_obj(content=content, filename=filename, suffix=suffix)


def random_text_file(filename=None, suffix='.txt'):
    """
    Return a random plaintext file-like object.
    """
    content = '\n\n'.join(lorem_ipsum.paragraphs(20))
    return random_file_obj(content=content, filename=filename, suffix=suffix)


def random_file_obj(content=None, content_length=None, filename=None,
                    filename_length=8, suffix='.bin'):
    """
    A random file-like object.
    """
    if content_length is None:
        content_length = 4096
    if filename is None:
        filename = random_filename(filename_length, suffix)
    if content is None:
        content = random_bytes(content_length)
    file_obj = StringIO.StringIO(content)
    file_obj.size = len(content)
    file_obj.name = filename
    return file_obj


def random_unicode(length, chars=LOTS_OF_UNICODE_CHARS):
    """
    A random unicode string made up from the given characters.
    """
    return u''.join([random.choice(chars) for idx in range(length)])


def random_bytes(length):
    """
    A random bytearray of given length.
    """
    return bytearray([random.randint(0, 255) for idx in range(length)])
