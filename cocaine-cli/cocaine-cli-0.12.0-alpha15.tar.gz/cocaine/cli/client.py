
import urlparse
import requests
import logging

from .util import normalize_url

class BaseClient(object):

    _api_version = (0,0,7)
    
    def __init__(self, **rc):
        self.base_url = rc.get("base")
        self.token = rc.get("token")
        self.user = rc.get("user")
        self.debug = rc.get("debug")


    def _handle_streaming_response(r):
        print "response", r
        print "headers", r.headers
        status = 0
        for ch in r.iter_lines(chunk_size=1):
            logging.debug("got chunk %s"%ch)
            try:
                r = json.loads(ch)
                if "error" in r and r["error"]:
                    print r["message"]

                    if DEBUG:
                        print r["traceback"]
                else:
                    if "b64" in r and r["b64"]:
                        m = r["message"].decode("base64")
                    else:
                        m = r["message"]
                    print m
            except Exception:
                print ch


    def _handle_response(self, r):
        return
        print r
        print r.text

    def _call():
        pass

    def _get(self, url, **kwargs):
        return self._request("get", url, **kwargs)

    def _put(self, url, update=False, **kwargs):
        return self._request("put", url, **kwargs)

    def _request(self, method, url, stream=True, **kwargs):
        params1 = {
            "token": self.token,
            "user": self.user,
            "debug": self.debug,
        }

        if "params" in kwargs:
            kwargs["params"].update(params1)
        else:
            kwargs["params"] = params1

        url = self.base_url+url
        url = normalize_url(url)

        r = requests.request(method, url, **kwargs)

        if stream:
            self._handle_streaming_response(r)
        else:
            self._handle_response(r)
            return r


            
class Client(BaseClient):

    def __init__(self, *args, **kwargs):
        super(Client, self).__init__(*args, **kwargs)


    def create(self, project_def):
        project_id = project_def["project_id"]
        r = self._put("project/%s"%project_id, project_def)
        self._handle_response(r)


    def push(self, version_def):
        project_id = project_def["name"]
        version_tag = project_def["version"]
        self._put("project/%s/version/%s"%(project_id,version_tag), json=version_def)
        self._post("project/%s/version/%s/build"%(project_id,version_tag))


    def build(self, project_id, version_tag):
        project_id = project_def["name"]
        version_tag = project_def["version"]
        r = self._post("project/%s/version/%s/build"%(project_id,version_tag))
        self._handle_streaming_response(r)


    def deploy(self, project_id, version_tag, cluster_id):
        project_id = project_def["name"]
        version_tag = project_def["version"]
        r = self._post("project/%s/version/%s/cluster/%s/deploy"%(project_id,version_tag,cluster_id))
        self._handle_streaming_response(r)


    def balance(self, project_id, cluster_id, routing):
        project_id = project_def["name"]
        r = self._post("project/%s/version/%s/build"%(project_id,version_tag))
        self._handle_streaming_response(r)


    def kibana(self, project_id, cluster_id):
        pass


    def deliver(self, project_id, version_id, cluster_id):
        pass


