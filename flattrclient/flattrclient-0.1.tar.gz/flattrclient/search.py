import flattrclient
import flattrclient.things

class SearchResult(flattrclient.resource.Resource):
    """ flattr search result. Contains things """

    def __init__(self, session=None, total_items=None, items=None, page=None,
                 things=None, **kwargs):
        """ Initialize with data of an dictionary

        :param session: `requests.session.Session`.
        :param total_items: Total number of items of the search result.
        :param items: Currently shown item.
        :param page: Page n of itmes-batch.
        :param things: List of found things.
        """
        # ignored fields: kwargs
        # so lib will not break if flattr-api adds a new field
        super(SearchResult, self).__init__(session)

        self._total_items = total_items
        self._items = items
        self._page = page
        self._things = (flattrclient.things.Thing(session=self._session, dirty=False, **elm) for elm in things)

    # Most of the fields are readonly since you can not modify them on flattr
    @property
    def total_items(self):
        """ Returns total_items """
        return getattr(self, '_total_items', None)

    @property
    def items(self):
        """ Returns items """
        return getattr(self, '_items', None)

    @property
    def page(self):
        """ Returns page """
        return getattr(self, '_page', None)

    @property
    def things(self):
        """ Returns things """
        return getattr(self, '_things', None)
