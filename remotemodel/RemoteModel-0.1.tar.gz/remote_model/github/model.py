from remote_model.model import AsyncList
from remote_model import RemoteModel


github_key = None


def get_key():
    return github_key


def set_key(value):
    global github_key
    github_key = value


github_api_url = "api.github.com"


class GithubModel(RemoteModel):
    def get_headers(self):
        headers = {
            "Accept": "application/vnd.github.v3+json",
            "User-Agent": self.agent
        }

        if self.key is not None:
            headers["Authorization"] = "token %s" % self.key

        return headers

    def parse(self, json, cache):
        if type(json) == AsyncList:
            # Hack to make it so we don't autoload whole list of items
            json = json._backing
        if type(json) == list:
            for obj in json:
                if "url" in obj:
                    cache(obj["url"], obj)
                self.parse(obj, cache)
        else:
            # it's a dict
            to_remove = {}
            for field in json:
                if len(field) > 3 and "url" in field and json[field] is not None and GithubModel.validate_url(json[field]):
                    to_remove[field] = GithubModel(url=json[field], key=self.key, ua=self.agent)
                else:
                    if type(json[field]) in (list, dict, AsyncList):
                        self.parse(json[field], cache)
            for field in to_remove:
                del json[field]
                json[field[:-4]] = to_remove[field]

    @staticmethod
    def validate_url(url):
        if "://" not in url:
            protocol = "https"
        else:
            protocol, url = url.split("://")

        if "{/" in url:
            url = url[:url.index("{/")]

        url_parts = url.split("/")

        if url_parts[0]:
            if url_parts[0] != github_api_url:
                return False

        url_parts = url_parts[1:]

        return "{protocol}://{domain}/{path}".format(protocol=protocol, domain=github_api_url, path="/".join(url_parts))

    def __init__(self, url=None, key=None, ua="Chaosphere2112GithubModelClient"):
        if key is None:
            key = get_key()
        self.key = key
        self.agent = ua
        super(GithubModel, self).__init__(url=url)
