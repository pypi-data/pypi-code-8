from .api import get_items_api


class KongUser(object):
    def __init__(self, api_key, user_id=None, username=None):
        self.api_key = api_key
        if username is None and user_id is None:
            return ValueError("Provide user_id or username")

        if user_id is not None:
            self.user_id = user_id

        self._items = None

        if username is not None:
            raise NotImplemented()

    def items(self, refetch=True):
        if self._items and not refetch:
            return self._items
        response = get_items_api(self.user_id, self.api_key)
        new_items = map(lambda x: Item(**x), response['items'])
        self._items = new_items
        return new_items

    def has_item(self, id=None, identifier=None):

        def _id_filter(x):
            return x.id == id

        def _identifier_filter(x):
            return x.identifier == identifier

        if id is None and identifier is None:
            return ValueError("Provide id or identifier")
        if id is not None:
            filter_key = _id_filter
        else:
            # identifer is not None
            filter_key = _identifier_filter

        items = filter(filter_key, self.items(refetch=False))
        return bool(items)


class Item(object):
    def __init__(
        self, id, identifier,
        name, description, remaining_uses,
        data
    ):
        self.id = id
        self.identifier = identifier
        self.name = name
        self.description = description
        self.remaining_uses = remaining_uses
        self.data = data

