from . import api_base, util
import requests

DOMAIN_NAME_ERROR = "domain_name must be a string representing a domain name, e.g. 'example.com'"
HTML_ERROR = "html must be a string"

class Requestor(object):
    def __init__(self, api_key=None):
        self.api_key = api_key

    def req(self, method, path, **kwargs):
        if self.api_key:
            the_key = self.api_key
        else:
            from . import api_key
            the_key = api_key

        if the_key is None:
            raise Exception(
                "No API key provided. Set your API key like so: "
                "\"picnic.api_key = <API_KEY>\". "
                "You can get an API key at https://picnic.sh/api. "
                "Remember, you can always ask us anything at help@picnic.sh."
            )

        api_key_header = {'X-Picnic-Api-Key': the_key}
        abs_url = '{}{}'.format(api_base, path)
        body = kwargs and {}
        for key, value in kwargs.items():
            body[key] = value
        resp = requests.request(method, abs_url, json=body, headers=api_key_header)
        return resp

class DictObj(dict):
    def __init__(self, dictlike=None):
        super(DictObj, self).__init__()
        if dictlike:
            self.construct_from(dictlike)

    def __setattr__(self, key, value):
        self[key] = value

    def __getattr__(self, key):
        try:
            return self[key]
        except KeyError as e:
            raise AttributeError(*e.args)

    def __setitem__(self, key, value):
        super(DictObj, self).__setitem__(key, value)

    def __getitem__(self, key):
        return super(DictObj, self).__getitem__(key)

    def __repr__(self):
        return str(self)

    def __str__(self):
        return util.json.dumps(self, sort_keys=True, indent=2)

    def construct_from(self, dictlike):
        for key, value in dictlike.items():
            if value and key.endswith('_at'):
                value = int(value)
            self[key] = value

class Website(DictObj):
    def update_content(self, html):
        resp = req('PUT', '/websites/{}'.format(self.domain_name), html=html)
        self.construct_from(resp.json())
        return self

class DomainStatus(DictObj):
    pass

_r = Requestor()
def req(*args, **kwargs):
    return _r.req(*args, **kwargs)

def list_websites():
    resp = req('GET', '/websites/')
    return [Website(w) for w in resp.json()]

def get_website(domain_name):
    if not domain_name:
        raise ValueError(DOMAIN_NAME_ERROR)

    resp = req('GET', '/websites/{}'.format(domain_name))
    return Website(resp.json())

def get_price(domain_name):
    if not domain_name:
        raise ValueError(DOMAIN_NAME_ERROR)

    resp = req('GET', '/price/{}'.format(domain_name))
    return DomainStatus(resp.json())

def create_website(domain_name, html):
    if not domain_name:
        raise ValueError(DOMAIN_NAME_ERROR)

    if not html:
        raise ValueError(HTML_ERROR)

    resp = req('POST', '/websites/', domain_name=domain_name, html=html)
    return Website(resp.json())

