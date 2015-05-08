# (c) 2011 Bright Interactive Limited. All rights reserved.
# http://www.bright-interactive.com | info@bright-interactive.com

from django import template
from django.http import QueryDict

register = template.Library()


@register.simple_tag(takes_context=True)
def remove_tag_from_url(context, tag):
    # Use copies of the form data to avoid manipulating the current form state
    cleaned_tags_list = []
    cleaned_tags_list.extend(context['form'].cleaned_data['tags'])
    query_dict = context['form'].data.copy()

    if tag in cleaned_tags_list:
        cleaned_tags_list.remove(tag)
        tags = ", ".join(cleaned_tags_list)
        query_dict['tags'] = tags
        query_dict.pop('more_tags', None)

    if not hasattr(query_dict, 'urlencode'):
        # it's a plain dict, not a QueryDict, so put it in a QueryDict
        new_query_dict = QueryDict(None, mutable=True)
        new_query_dict.update(query_dict)
        query_dict = new_query_dict
    return query_dict.urlencode()
