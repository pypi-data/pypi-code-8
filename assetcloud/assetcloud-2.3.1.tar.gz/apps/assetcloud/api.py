# -*- coding: utf-8 -*-
# (c) 2011 Bright Interactive Limited. All rights reserved.
# http://www.bright-interactive.com | info@bright-interactive.com

"""
API views
"""

from django.http import HttpResponse
from assetcloud.views import get_asset_or_error
import assetcloud_auth


@assetcloud_auth.require_can_edit_assets
def asset_title_action(request, id):
    asset = get_asset_or_error(id, request.user)

    asset.title = request.POST['title']
    asset.save()

    return HttpResponse()
