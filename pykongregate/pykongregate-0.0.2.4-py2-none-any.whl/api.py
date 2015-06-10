import requests
import simplejson
from simplejson.scanner import JSONDecodeError

from .exceptions import NullResponseException


GET_USER_ITEMS_URL = "http://www.kongregate.com/api/user_items.json"
GET_ITEMS_URL = "http://www.kongregate.com/api/items.json"
USER_INFO_URL = "http://www.kongregate.com/api/user_info.json"


def _handle_request(url, params):
    response = requests.get(
        GET_USER_ITEMS_URL, params=params
    )
    try:
        return simplejson.loads(response.text)
    except JSONDecodeError:
        raise NullResponseException(
            "request_url: {url}. params: {params}. "
            "Got unparsable response: {response}".format(
                url=url,
                params=params,
                response=response.text,
            )
        )


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
    url = GET_USER_ITEMS_URL
    return _handle_request(url, params)


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
    url = GET_ITEMS_URL
    return _handle_request(url, params)


def get_user_info_api(username):
    """
    wrapper on API method:
    http://developers.kongregate.com/docs/rest/user_info

    :param username:
    :type username: str

    :rtype: dict
    :return: loaded json from response
    """
    # TODO: implement all params
    params = {
        'username': username
    }
    url = USER_INFO_URL
    return _handle_request(url, params)
