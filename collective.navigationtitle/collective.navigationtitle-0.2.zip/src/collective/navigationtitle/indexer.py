from .behavior import INavigationTitle
from plone.indexer import indexer


@indexer(INavigationTitle)
def short_title(obj):
    ob = INavigationTitle(obj, None)
    if ob is None:
        return None
    return ob.short_title
