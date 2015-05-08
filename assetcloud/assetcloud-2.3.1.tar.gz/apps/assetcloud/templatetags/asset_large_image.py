# -*- coding: utf-8 -*-
# (c) 2012 Bright Interactive Limited. All rights reserved.
# http://www.bright-interactive.com | info@bright-interactive.com

from django import template
from django.template.context import Context
from django.template.loader import get_template

register = template.Library()


@register.simple_tag()
def asset_large_image(asset, geometry):
    """
    Render an asset thumbnail, or an icon if the file isn't an image, or a
    "broken" icon if it is an image but we can't generate a thumbnail.
    """
    template = get_template('assetcloud/snippets/asset_large_image.html')
    context = Context()
    context['asset'] = asset
    context['geometry'] = geometry
    result = template.render(context)
    return result
