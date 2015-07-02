__author__ = 'ca1ek'

import requests

company_types = {0: "none",
                 1: "grain",
                 2: "food",
                 3: "fruit",
                 4: "juice",
                 5: "iron",
                 6: "weapon",
                 7: "oil",
                 8: "moving ticket",
                 9: "wood",
                 10: "house",
                 11: "hospital",
                 12: "defense system",
                 13: "hotel",
                 14: "construction"}


def get_from_api(link):
    r = requests.get(link)
    if r.status_code == 503:
        raise APIUnavailable("HTTP Error 503 - Service unavailable")
    else:
        return r.json()


class APIError(Exception):
    pass


class APIUnavailable(Exception):
    pass


class Citizen:
    def __init__(self, citizen_id):
        if type(citizen_id) is str:
            json = get_from_api("http://api.vpopulus.net/v1/feeds/citizen.json?name=" + citizen_id)
            self.using_new_api = False
        elif type(citizen_id) is int:
            try:
                json = get_from_api("http://api.vpopulus.net/v1/feeds/citizen.json?id=" + str(citizen_id))
                self.using_new_api = False
            except APIUnavailable:
                json = get_from_api("http://newapi.vpopulus.net/api/citizen/getByID/" + str(citizen_id))["citizen"]
                self.using_new_api = True

        if 'message' in json:
            raise APIError(json["message"])

        self.raw_json = json
        self.id = int(json["id"])
        self.name = json["name"]
        self.experience = json["experience"]
        if self.using_new_api:
            self.avatar_url = json["avatar"]
        else:
            self.avatar_url = json["avatar-link"]
        self.wellness = int(json["wellness"])
        self.skills = json["skills"]
        self.citizenship = json["citizenship"]["country"]
        self.location = json["location"]["country"]
        self.region = json["location"]["region"]
        self.company = json["company"]
        self.party = json["party"]
        self.army = json["army"]
        if self.using_new_api:
            self.newspaper = None
        else:
            self.newspaper = json["newspaper"]
        if self.using_new_api:
            self.date_of_birth = json["creation_date"]
        else:
            self.date_of_birth = json["date-of-birth"]

    def look_up_company(self):
        return Company(self.company["id"])


class Company:
    def __init__(self, company_id):
        if type(company_id) is str:
            json = get_from_api("http://api.vpopulus.net/v1/feeds/company.json?name=" + company_id)
        elif type(company_id) is int:
            json = get_from_api("http://api.vpopulus.net/v1/feeds/company.json?id=" + str(company_id))

        if 'message' in json:
            raise APIError(json["message"])

        self.raw_json = json
        self.id = json["id"]
        self.name = json["name"]
        self.avatar_url = json["avatar-link"]
        self.location = json["location"]["country"]
        self.region = json["location"]["region"]
        self.type = json["type"]["id"]
        self.quality = json["quality"]
        self.stock = json["stock"]
        self.queue = json["queue"]
        self.materials = json["materials"]
        self.employee_count = json["employee-count"]
        self.job_offers = json["job-offers"]        # TODO: more detailed data returned if possible
        self.market_offers = json["market-offers"]  # TODO: more detailed data returned if possible


class Raw:
    def __init__(self, url):
        self.request = requests.get(url)
        if self.request.status_code == 503:
            raise APIUnavailable("HTTP Error 503 - Service unavailable")
        else:
            self.json = self.request.json()