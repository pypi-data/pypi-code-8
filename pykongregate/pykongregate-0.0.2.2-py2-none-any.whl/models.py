from .api import get_items_api, get_user_items_api
from .exceptions import ApiException


class KongApi(object):
    """
    Kongregate API wrapper class.

    :param api_key:
    :type api_key: str
    """
    def __init__(self, api_key):
        self.api_key = api_key

    def get_user_items(self, user):
        """
        get items for user

        :param user:
        :type user: KongUser

        :rtype: list of KongUserItem
        :return: items list
        """
        response = self.api_call(
            get_user_items_api,
            user.user_id, self.api_key
        )
        new_items = map(
            lambda x: KongUserItem(**x),
            response['items']
        )
        return new_items

    def get_items(self):
        """
        get available items

        :rtype: list of KongItem
        :return: items list
        """
        response = self.api_call(
            get_items_api,
            self.api_key
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
        new_items = self.api.get_user_items(self)
        self._items = new_items
        return new_items

    def has_item(self, id=None, identifier=None):
        """
        Determines if user has item with criteria.

        :param id: unique transaction_id of kongregate.
        :type id: int
        :param identifier: bank_item name. User can buy several of them.
            Return True if at least one is there.
        :type identifier: str

        :rtype: bool
        :return:
        """
        def _id_filter(x):
            return x.id == id

        def _identifier_filter(x):
            return x.identifier == identifier

        if id is None and identifier is None:
            return ValueError("Provide id or identifier")

        items = self.items()
        if id is not None:
            items = filter(_id_filter, items)
        if identifier is not None:
            items = filter(_identifier_filter, items)

        return bool(items)

    def __repr__(self):
        return "KongUser: {}".format(self.user_id)


class KongBaseItem(object):
    def __init__(
        self,
        id=None,
        identifier=None,
        name=None,
        description=None,
        **kwargs
    ):
        self.id = id
        self.identifier = identifier
        self.name = name
        self.description = description

        for k, v in kwargs.items():
            setattr(self, k, v)

    def __repr__(self):
        return "{}: [id:{}, identifier: {}]".format(
            self.__class__.__name__,
            self.id,
            self.identifier
        )


class KongUserItem(KongBaseItem):
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
        self,
        id=None,
        identifier=None,
        name=None,
        description=None,
        remaining_uses=None,
        data=None,
        **kwargs
    ):
        super(KongUserItem, self).__init__(
            id=id,
            identifier=identifier,
            name=name,
            description=description,
            **kwargs
        )
        self.remaining_uses = remaining_uses
        self.data = data


class KongItem(KongBaseItem):
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
    :param price:
    :type price:
    :param tags:
    :type tags:
    """
    def __init__(
        self,
        id=None,
        identifier=None,
        name=None,
        description=None,
        price=None,
        tags=None,
        **kwargs
    ):
        super(KongItem, self).__init__(
            id=id,
            identifier=identifier,
            name=name,
            description=description,
            **kwargs
        )
        self.price = price
        self.tags = tags
