from zope.interface import Interface

# Storage
from eea.faceted.tool.storage.interfaces import IPortalType

# Catalog
from eea.faceted.tool.search.interfaces import IFacetedCatalog

class IFacetedTool(Interface):
    """ Faceted Tool
    """
