#coding:utf-8
import os
import logging

from django.template.base import Library
from django.conf import settings
from django.utils.encoding import smart_str, force_unicode
from django.utils.safestring import mark_safe

logger = logging.getLogger(__name__)

register = Library()

def static(context, link_url):
    """
    Get the path for a static file in the Cactus build.
    We'll need this because paths can be rewritten with fingerprinting.
    """
    #TODO: Support URLS that don't start with `/static/`
    site = context['__CACTUS_SITE__']
    page = context['__CACTUS_CURRENT_PAGE__']

    url = site.get_url_for_static(link_url)

    if url is None:

        # For the static method we check if we need to add a prefix
        helper_keys = [
            "/static/" + link_url,
            "/static"  + link_url,
            "static/"  + link_url
        ]

        for helper_key in helper_keys:
            
            url_helper_key = site.get_url_for_static(helper_key)

            if url_helper_key is not None:
                return url_helper_key
                
        logger.warn('%s: static resource does not exist: %s', page.link_url, link_url)
        
        url = link_url

    return url

def url(context, link_url):
    """
    Get the path for a page in the Cactus build.
    We'll need this because paths can be rewritten with prettifying.
    """
    site = context['__CACTUS_SITE__']
    page = context['__CACTUS_CURRENT_PAGE__']

    url = site.get_url_for_page(link_url)

    if url is None:

        # See if we're trying to link to an /subdir/index.html with /subdir
        link_url_index = os.path.join(link_url, "index.html")
        url_link_url_index = site.get_url_for_page(link_url_index)

        if url_link_url_index is None:
            logger.warn('%s: page resource does not exist: %s', page.link_url, link_url)
        
        url = link_url

    if site.prettify_urls:
        return url.rsplit('index.html', 1)[0]

    return url

def config(context, key):
    """
    Get a value from the config by key
    """
    site = context['__CACTUS_SITE__']
    result = site.config.get(key)

    if result:
        return result

    return ""


def current_page(context):
    """
    Returns the current URL
    """
    page = context['__CACTUS_CURRENT_PAGE__']

    return page.final_url


def if_current_page(context, link_url, positive=True, negative=False):
    """
    Return one of the passed parameters if the URL passed is the current one.
    For consistency reasons, we use the link_url of the page.
    """
    page = context['__CACTUS_CURRENT_PAGE__']

    return positive if page.link_url == link_url else negative

@register.filter(is_safe=True)
def markdown(value, arg=''):
    """
    Runs Markdown over a given value, optionally using various
    extensions python-markdown supports.

    Syntax::

        {{ value|markdown2:"extension1_name,extension2_name..." }}

    To enable safe mode, which strips raw HTML and only returns HTML
    generated by actual Markdown syntax, pass "safe" as the first
    extension in the list.

    If the version of Markdown in use does not support extensions,
    they will be silently ignored.

    """
    try:
        import markdown2
    except ImportError:
        logging.warning("Markdown package not installed.")
        return force_unicode(value)
    else:
        def parse_extra(extra):
            if ':' not in extra:
                return (extra, {})
            name, values = extra.split(':', 1)
            values = dict((str(val.strip()), True) for val in values.split('|'))
            return (name.strip(), values)

        extras = (e.strip() for e in arg.split(','))
        extras = dict(parse_extra(e) for e in extras if e)

        if 'safe' in extras:
            del extras['safe']
            safe_mode = True
        else:
            safe_mode = False

        return mark_safe(markdown2.markdown(force_unicode(value), extras=extras, safe_mode=safe_mode))

register.simple_tag(takes_context=True)(static)
register.simple_tag(takes_context=True)(url)
register.simple_tag(takes_context=True)(config)
register.simple_tag(takes_context=True)(current_page)
register.simple_tag(takes_context=True)(if_current_page)
