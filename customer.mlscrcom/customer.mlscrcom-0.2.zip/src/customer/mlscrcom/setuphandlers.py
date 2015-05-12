# -*- coding: utf-8 -*-

###############################################################################
#
# Copyright (c) 2011 Propertyshelf, Inc. and its Contributors.
# All Rights Reserved.
#
# This program is free software; you can redistribute it and/or modify it under
# the terms of the GNU General Public License version 2 as published by the
# Free Software Foundation.
#
# This program is distributed in the hope that it will be useful, but WITHOUT
# ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS
# FOR A PARTICULAR PURPOSE. See the GNU General Public License for more
# details.
#
# You should have received a copy of the GNU General Public License along with
# this program; if not, write to the Free Software Foundation, Inc.,
# 51 Franklin Street, Fifth Floor, Boston, MA  02110-1301, USA.
#
###############################################################################
"""Additional setup steps."""

# python imports
from logging import getLogger
import transaction

# zope imports
from Products.CMFCore.utils import getToolByName
from Products.CMFCore.WorkflowCore import WorkflowException


logger = getLogger('customer.mlscrcom')


def setup_linguaplone(context):
    """Setup the multilingual environment."""
    if context.readDataFile('customer.mlscrcom.txt') is None:
        return

    site = context.getSite()
    portal_languages = getToolByName(site, 'portal_languages')

    # Set the default language of the front page if it is neutral.
    defaultPageID = site.getDefaultPage()
    if defaultPageID is not None:
        defaultPage = getattr(site, defaultPageID)
        if defaultPage is not None:
            language = defaultPage.Language()
            if language is None:
                defaultPage.setLanguage(portal_languages.getDefaultLanguage())

    transaction.commit()
    # Run the LinguaPlone setup script
    view = site.restrictedTraverse('@@language-setup-folders')
    try:
        view()
    except WorkflowException:
        logger.warn('No workflow found. LinguaPlone was not set up correctly!')
