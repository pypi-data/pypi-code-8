from .api import get_items_api
from .exceptions import ApiException


class KongApi(object):
    """
    Kongregate API wrapper class.

    :param api_key:
    :type api_key: str
    """
    def __init__(self, api_key):
        self.api_key = api_key

    def get_items(self, user):
        """
        get items for user

        :param user:
        :type user: KongUser

        :rtype: list of KongItem
        :return: items list
        """
        response = self.api_call(
            get_items_api,
            user.user_id, self.api_key
        )
        new_items = map(
            lambda x: KongItem(**x),
            response['items']
        )
        return new_items

    def api_call(self, method, *args, **kwargs):
        """
        api call wrapper.

        :param method: kongregate api method from .api
        :type method: func

        :rtype: dict
        :return: response, loaded response json in dict.
        :raises ApiException: raise error with description if smth gone wrong
        """
        response = method(*args, **kwargs)
        if response['success'] is False:
            raise ApiException(
                response['error_description']
            )
        return response


class KongUser(object):
    """
    Kongregate User wrapper class.
    user user_id or username.
    if both provided: only user_id will be used.

    :param api_key:
    :type api_key: str
    :param user_id: kongregate user_id
    :type user_id: int
    :param username: kongregate username
    :type username: str
    """
    def __init__(self, api_key, user_id=None, username=None):
        self.api = KongApi(api_key)
        if username is None and user_id is None:
            return ValueError("Provide user_id or username")

        if user_id is not None:
            self.user_id = user_id

        self._items = None

        if username is not None:
            raise NotImplemented()

    def items(self, refetch=True):
        """
        Return items of user
        :param refetch:
            True: fetch kongregate
            False: fetch kongregate only if items is not cached
        :type refetch: bool

        :rtype: list of KongItem
        :return:
        """
        if self._items and not refetch:
            return self._items
        new_items = self.api.get_items(self)
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


class KongItem(object):
    """
    Kongregate user item

    :param id:
    :type id:
    :param identifier:
    :type identifier:
    :param name:
    :type name:
    :param description:
    :type description:
    :param remaining_uses:
    :type remaining_uses:
    :param data:
    :type data:
    """
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

