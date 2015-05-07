# -*- coding: utf-8 -*-
# (c) 2012 Bright Interactive Limited. All rights reserved.
# http://www.bright-interactive.com | info@bright-interactive.com
import logging


logger = logging.getLogger(__name__)


class Navigation(object):
    def __init__(self, request):
        self.request = request

    @property
    def asset_list_url(self):
        url = self.request.session.get('asset_list_url', None)
        logger.debug('asset_list_url returning %s', url)
        return url

    def current_page_is_asset_list(self):
        """
        Let the Navigation know that the current request is for an asset list
        page so it should update asset_list_url.
        """
        url = self.request.get_full_path()
        logger.debug('setting asset_list_url to %s', url)
        self.request.session['asset_list_url'] = url
