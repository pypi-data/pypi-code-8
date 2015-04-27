import requests
import simplejson


GET_ITEMS_URL = "http://www.kongregate.com/api/user_items.json"


def get_items_api(user_id, api_key):
    params = {
        'api_key': api_key,
        'user_id': user_id,
    }
    response = requests.get(
        GET_ITEMS_URL, params=params
    )
    # TODO: process errors
    # u'{"success":false,"error":400,"error_description":"Required: game_id"}'
    return simplejson.loads(response.text)
