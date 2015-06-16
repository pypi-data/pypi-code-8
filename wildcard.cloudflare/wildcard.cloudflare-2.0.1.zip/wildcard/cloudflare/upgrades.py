from Products.CMFCore.utils import getToolByName


PROFILE_ID = 'profile-wildcard.cloudflare:default'


def upgrade_20(context, logger=None):
    setup = getToolByName(context, 'portal_setup')
    setup.runImportStepFromProfile(PROFILE_ID, 'plone.app.registry')