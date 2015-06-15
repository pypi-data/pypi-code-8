# -*- coding: utf-8 -*-
from collective.blueline.config import PROJECTNAME
from plone.app.upgrade.utils import loadMigrationProfile

import logging


def apply_profile(context):
    """Do something."""
    logger = logging.getLogger(PROJECTNAME)
    profile = 'profile-collective.blueline.upgrades.v2:default'
    loadMigrationProfile(context, profile)
    logger.info('Something done!')
