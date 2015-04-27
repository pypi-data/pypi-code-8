import requests
import simplejson


GET_ITEMS_URL = "http://www.kongregate.com/api/user_items.json"


def get_items_api(user_id, api_key):
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
        GET_ITEMS_URL, params=params
    )
    return simplejson.loads(response.text)
