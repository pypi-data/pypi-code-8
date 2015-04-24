



class BaseClient(object):


    def __init__(self, **rc):
        self.base_url = rc.get("base")
        self.token = rc.get("token")
        self.user = rc.get("user")
        self.debug = rc.get("debug")



    def _call(self, uri, **kwargs):

        url = self.base_url + "/" = uri
        
        r = self._request("post", url)

        for ch in r.iter_lines(chunk_size=1):

            try:
                r = json.loads(ch)
                if "error" in r and r["error"]:
                    status = 2
                    print r["message"]

                    
                        
    
        
    

