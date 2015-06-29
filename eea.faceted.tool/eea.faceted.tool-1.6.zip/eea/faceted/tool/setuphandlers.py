from Products.CMFCore.utils import getToolByName

def addObjectProvidesIndex(portal):
    """Add the object_provides index to the portal_catalog.
    """
    catalog = getToolByName(portal, 'portal_catalog')
    if 'object_provides' not in catalog.indexes():
        catalog.addIndex('object_provides', 'KeywordIndex')

def setupVarious(context):
    """ Do some various setup.
    """
    if context.readDataFile('eeafacetedtool.txt') is None:
        return

    portal = context.getSite()

    # Add object_provides index
    addObjectProvidesIndex(portal)
