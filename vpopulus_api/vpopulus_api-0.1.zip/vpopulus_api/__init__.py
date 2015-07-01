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


class APIError(Exception):
    pass


class Citizen:
    def __init__(self, search_by, citizen_id):
        if search_by == "name":
            json = requests.get("http://api.vpopulus.net/v1/feeds/citizen.json?name=" + citizen_id).json()
        elif search_by == "id":
            json = requests.get("http://api.vpopulus.net/v1/feeds/citizen.json?id=" + citizen_id).json()

        if 'message' in json:
            raise APIError(json["message"])

        self.raw_json = json
        self.id = json["id"]
        self.name = json["name"]
        self.avatar_url = json["avatar-link"]
        self.wellness = json["wellness"]
        self.skills = json["skills"]
        self.citizenship = json["citizenship"]["country"]
        self.location = json["location"]["country"]
        self.region = json["location"]["region"]
        self.company = json["company"]
        self.party = json["party"]
        self.army = json["army"]
        self.newspaper = json["newspaper"]
        self.date_of_birth = json["date-of-birth"]


class Company:
    def __init__(self, search_by, company_id):
        if search_by == "name":
            json = requests.get("http://api.vpopulus.net/v1/feeds/company.json?name=" + company_id).json()
        elif search_by == "id":
            json = requests.get("http://api.vpopulus.net/v1/feeds/company.json?id=" + company_id).json()

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
        self.json = self.request.json()





