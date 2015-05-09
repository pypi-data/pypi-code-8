# -*- coding: utf-8 -*-
import os
import json
import time
import requests

FEDERAL_FACILITIES = {}
with open(os.path.join(os.path.dirname(__file__), "..", "data", "federal.json")) as fh:
    data = json.load(fh)
    for facility in data:
        FEDERAL_FACILITIES[facility['identifier']] = facility

def search(**kwargs):
    url = "http://www.bop.gov/PublicInfo/execute/inmateloc"

    searches = []
    if kwargs.get('number'):
        for numtype in ("IRN", "DCDC", "FBI", "INS"):
            searches.append({"inmateNum": kwargs['number'], "inmateNumType": numtype})
    else:
        searches.append({"nameFirst": kwargs.get("first_name"), "nameLast": kwargs.get("last_name")})

    results = []
    errors = []

    for i,search in enumerate(searches):
        search['todo'] = 'query'
        search['output'] = 'json'
        res = requests.get(url, params=search)
        if res.status_code != 200:
            errors.append(res.content)
            break

        data = json.loads(res.content)
        if 'InmateLocator' not in data:
            errors.append(res.content)
            continue
        for result in data['InmateLocator']:
            result['name'] = u"{} {}".format(result['nameFirst'], result['nameLast'])
            if 'faclURL' in result:
                result['facility URL'] = "http://www.bop.gov{}".format(result['faclURL'])
            if result.get('faclCode'):
                result['address'] = FEDERAL_FACILITIES[result['faclCode']]
            results.append(result)

    return {"state": "Federal", "results": results, "errors": errors, "url": url}

