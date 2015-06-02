import requests
import json

def avatar_url(size='normal'):
    if size not in ['normal','epic','bigger','mini']:
        raise Exception, 'Argument must be normal, epic, bigger or mini'
    req = requests.get("http://uifaces.com/api/v1/random")
    j = json.loads(req.content)
    return j['image_urls'][size]



