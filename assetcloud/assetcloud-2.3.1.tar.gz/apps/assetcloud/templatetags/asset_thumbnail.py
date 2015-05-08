from assetcloud.templatetags.asset_large_image import asset_large_image
from django import template

import warnings

register = template.Library()

warnings.warn("assetcloud.templatetags.asset_thumbnail is deprecated; use assetcloud.templatetags.asset_large_image instead", DeprecationWarning)

asset_thumbnail = asset_large_image
register.simple_tag(asset_thumbnail, name="asset_thumbnail")
