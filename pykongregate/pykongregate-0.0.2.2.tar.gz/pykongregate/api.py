import requests
import simplejson


GET_USER_ITEMS_URL = "http://www.kongregate.com/api/user_items.json"
GET_ITEMS_URL = "http://www.kongregate.com/api/items.json"


def get_user_items_api(user_id, api_key):
    """
    wrapper on API method:
    http://developers.kongregate.com/docs/rest/user-items

    :param user_id:
    :type user_id: int
    :param api_key:
    :type api_key: str

    :rtype: dict
    :return: loaded json from response
    """
    params = {
        'api_key': api_key,
        'user_id': user_id,
    }
    response = requests.get(
        GET_USER_ITEMS_URL, params=params
    )
    return simplejson.loads(response.text)


def get_items_api(api_key):
    """
    wrapper on API method:
    http://developers.kongregate.com/docs/rest/items

    :param api_key:
    :type api_key: str

    :rtype: dict
    :return: loaded json from response
    """
    params = {
        'api_key': api_key,
    }
    response = requests.get(
        GET_ITEMS_URL, params=params
    )
    return simplejson.loads(response.text)
