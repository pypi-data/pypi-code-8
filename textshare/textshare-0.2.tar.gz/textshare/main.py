from __future__ import with_statement
import requests

def readfile(path):
    with open(path) as f:
        s = f.read()
    return s

def uploadfile(path):
    text_to_upload = readfile(path)
    res = requests.post("http://sprunge.us", params={"sprunge":text_to_upload})
    if res.status_code == 200:
        return res.text.rstrip("\r\n")
    else:
        return "Something is wrong please report it in https://github.com/bindingofisaac/textshare\n"
