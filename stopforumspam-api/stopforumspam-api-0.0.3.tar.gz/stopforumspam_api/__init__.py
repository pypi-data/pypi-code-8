import requests
from datetime import datetime

QUERY_API = "http://api.stopforumspam.org/api"
REPORT_API = "https://www.stopforumspam.com/add"


class ApiResponseSection(object):
    def __init__(self, response_section):
        self.section = response_section or {}

    @property
    def appears(self):
        return self.section.get("appears", 0) == 1

    @property
    def frequency(self):
        return self.section.get("frequency", None)

    @property
    def lastseen(self):
        if "lastseen" not in self.section:
            return None
        return datetime.strptime(self.section["lastseen"], "%Y-%m-%d %H:%M:%S")

    @property
    def confidence(self):
        return self.section.get("confidence", None)


class ApiResponse(object):
    def __init__(self, response_json):
        self.response = response_json

    @property
    def success(self):
        return self.response.get("success", 0) == 1

    @property
    def ip(self):
        return ApiResponseSection(self.response.get("ip", None))

    @property
    def email(self):
        return ApiResponseSection(self.response.get("email", None))

    @property
    def username(self):
        return ApiResponseSection(self.response.get("username", None))

    def confidence(self, func=max):
        return func(self.ip.confidence, self.email.confidence, self.username.confidence)

    def frequency(self, func=max):
        return func(self.ip.frequency, self.email.frequency, self.username.frequency)

    def lastseen(self, func=max):
        dates = filter(bool, (self.ip.lastseen, self.email.lastseen, self.username.lastseen))
        return func(dates)

    def appears(self, func=any):
        return func((self.ip.lastseen, self.email.lastseen, self.username.lastseen))
        

def query(ip=None, email=None, username=None, api_url=QUERY_API):
    if not any((ip, email, username)):
        raise Exception("No query data supplied")

    params = dict(f="json")
    if ip:
        params["ip"] = ip
    if email:
        params["email"] = email
    if username:
        params["username"] = username
    
    try:
        response = requests.get(api_url, params=params).json()
    except requests.exceptions.ConnectionError:
        response = {}

    return ApiResponse(response)


def report(ip, email, username, key, evidence=None, api_url=REPORT_API):
    params = dict(ip=ip, email=email, username=username, api_key=key)

    if evidence:
        params["evidence"] = evidence

    response = requests.post(api_url, data=params)

    return response.status_code == 200
