from django import template
from django.core.urlresolvers import reverse
import decimal

register = template.Library()


@register.filter
def aspect_width(asset, height):
    """
    Return the width of the given asset if maintaining aspect ratio during a resize to height
    """
    iwidth, iheight = asset.image_info.width, asset.image_info.height
    width = decimal.Decimal(iwidth) / decimal.Decimal(iheight) * decimal.Decimal(height)

    return width.quantize(1)


@register.filter
def aspect_height(asset, width):
    """
    Return the height of the given asset if maintaining aspect ratio during a resize to width
    """
    iwidth, iheight = asset.image_info.width, asset.image_info.height
    height = decimal.Decimal(iheight) / decimal.Decimal(iwidth) * decimal.Decimal(width)

    return height.quantize(1)


@register.simple_tag()
def get_resize_bounds_within(asset, width, height=None):
    """
    Return the width and height of the given asset maintaing aspect ratio when resized to have a maximum dimension of dim
    """
    if height is None:
        height = width

    w, h, asset_w, asset_h = (decimal.Decimal(x)
                              for x
                              in (width, height, asset.image_info.width, asset.image_info.height))

    incoming_ratio, target_ratio = asset_w / asset_h, w / h

    # If the target is 'more landscapy' than the incoming asset, use width
    # otherwise use height
    factor = min(w, h) / (asset_w
                          if incoming_ratio > target_ratio
                          else asset_h)

    return ((factor * asset_w).quantize(1),
            (factor * asset_h).quantize(1))


@register.simple_tag()
def resize_url(asset, width, height=None):
    """
    Return a URL suitable for resizing the given asset to the given width and height
    """
    if height is None:
        return reverse('asset-resize-download-width-action',
                       args=[asset.id, width])
    else:
        return reverse('asset-resize-download-action',
                       args=[asset.id, width, height])
