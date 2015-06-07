from operator import itemgetter
from requests_futures.sessions import FuturesSession
from firebase_token_generator import create_token

request = FuturesSession()

class Firebase():
    """ Firebase Interface """
    def __init__(self, firebase_url, firebase_secret):

        if not firebase_url.endswith('/'):
            url = ''.join([firebase_url, '/'])
        else:
            url = firebase_url

        # get auth token
        auth_payload = {"uid": "1", "auth_data": "foo", "other_auth_data": "bar"}
        # disregard security rules
        options = {"admin": True}
        token = create_token(firebase_secret, auth_payload, options)

        self.fire_base_url = url
        self.token = token

    def info(self):
        return self.fire_base_url, self.token

    def all(self, child, callback):
        request_ref = '{0}{1}.json?auth={2}'.\
            format(self.fire_base_url, child, self.token)

        request_object = request.get(request_ref, background_callback=callback).result()

        request_json = request_object.json()

        if request_object.status_code != 200:
            raise ValueError(request_json)

        request_list = []

        # put dictionary in list for sorting
        for i in request_json:
            # add ID key and assign id
            request_json[i]["id"] = i
            request_list.append(request_json[i])

        return request_list

    def sort_by_first(self, child, category, start_at, limit_to_first, callback):
        if type(limit_to_first) is int:
            str(limit_to_first)

        request_ref = '{0}{1}.json?auth={2}&orderBy="{3}"&startAt={4}&limitToFirst={5}'.\
            format(self.fire_base_url, child, self.token, category, start_at, limit_to_first)

        request_object = request.get(request_ref, background_callback=callback).result()
        request_json = request_object.json()

        if request_object.status_code != 200:
            raise ValueError(request_json)

        request_list = []

        # put dictionary in list for sorting
        for i in request_json:
            # add ID key and assign id
            request_json[i]["id"] = i
            request_list.append(request_json[i])

        # sort list by time (datetime)
        request_list = sorted(request_list, key=itemgetter(category))

        return request_list

    def sort_by_last(self, child, category, start_at, limit_to_last, callback):
        if type(limit_to_last) is int:
            str(limit_to_last)

        if start_at:
            request_ref = '{0}{1}.json?auth={2}&orderBy="{3}"&endAt={4}&limitToLast={5}'.\
                format(self.fire_base_url, child, self.token, category, start_at, limit_to_last)
        else:
            request_ref = '{0}{1}.json?auth={2}&orderBy="{3}"&limitToLast={4}'.\
                format(self.fire_base_url, child, self.token, category, limit_to_last)

        request_object = request.get(request_ref, background_callback=callback).result()
        request_json = request_object.json()

        if request_object.status_code != 200:
            raise ValueError(request_json)

        request_list = []

        # put dictionary in list for sorting
        for i in request_json:
            # add ID key and assign id
            request_json[i]["id"] = i
            request_list.append(request_json[i])

        # sort list by time (datetime)
        request_list = sorted(request_list, key=itemgetter(category), reverse=True)

        return request_list


