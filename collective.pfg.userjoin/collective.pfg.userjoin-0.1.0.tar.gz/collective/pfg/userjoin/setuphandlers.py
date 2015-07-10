# -*- coding: utf-8 -*-

from Products.CMFCore.utils import getToolByName
from collective.pfg.userjoin import logger


def setupVarious(context):
    if context.readDataFile('collective.pfg.userjoin_various.txt') is None:
        return
    portal = context.getSite()
    setup_type(portal)
    pfg_tool = getToolByName(portal, 'formgen_tool')
    # Required to see the new validator if PFG was already installed when you added this add-on
    pfg_tool._initStringValidators()


def setup_type(portal):

    types = getToolByName(portal, 'portal_types')
    if 'FormFolder' in types.objectIds():
        folder = types['FormFolder']
        allowed_content_types = set(folder.allowed_content_types)
        allowed_content_types.add('UserJoinAdapter')
        folder.allowed_content_types = tuple(allowed_content_types)
        logger.info("UserJoinAdapter registered ad PloneFormGen adapter")    
