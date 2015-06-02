import requests
import json

def avatar_url(size='normal'):
    req = requests.get("http://uifaces.com/api/v1/random")
    j = json.loads(req.content)
    return j['image_urls'][size]

