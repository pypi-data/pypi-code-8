# -*- coding: utf-8 -*-
from plone import api
from plone.browserlayer import utils

import logging

logger = logging.getLogger('collective.js.cycle2')

JS_REGISTERED = (
    '++resource++collective.js.cycle2/jquery.cycle2.min.js',
    '++resource++collective.js.cycle2/jquery.cycle2.center.min.js',
    '++resource++collective.js.cycle2/jquery.cycle2.swipe.min.js'
)


def remove_profile_registrations(context):
    """Remove browser layer and JS resource registry registrations."""

    utils.unregister_layer('collective.js.cycle2')
    logger.info('Browser layer removed')

    js_tool = api.portal.get_tool('portal_javascripts')
    for js_id in JS_REGISTERED:
        js_tool.unregisterResource(js_id)
        logger.info('"{0}" resource was removed"'.format(js_id))
    js_tool.cookResources()
    logger.info('JS resources were cooked')
