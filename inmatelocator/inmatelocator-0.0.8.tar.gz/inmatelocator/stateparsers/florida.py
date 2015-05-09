# -*- coding: utf-8 -*-
import re
import requests
import lxml.html
from inmatelocator.utils import normalize_name, make_facility_lookup
from addresscleaner import format_address

# Load facility data.

# Mapping from things we get from the search API to normalized names from the
# directory.
facility_name_overrides = {
    'apalachee east unit': 'Apalachee Correctional Institution East',
    'apalachee west unit': 'Apalachee Correctional Institution West',
    'jackson work camp': 'Jackson Correctional Institution',
    'baker re entry centr': 'Baker Correctional Institution',
    'blackwater cf': 'Blackwater River Correctional Facility',
    'everglades re entry': 'Everglades Correctional Institution',
    'flwomens recpnctr': 'Florida Womens Reception Center',
    'okeechobee work camp': 'Okeechobee',
    'rmc main unit': 'Reception and Medical Center',
    'rmc west unit': 'Reception and Medical Center West Unit',
    'sago palm re entry c': 'Sago Palm Re-Entry Center',
    'sfrc': 'South Florida Reception Center',
    'suncoast crcfem': 'Suncoast Community Release Center',
}

def normalize_facility_name(name):
    name = normalize_name(name)
    if name in facility_name_overrides:
        return normalize_name(facility_name_overrides[name])
    name = re.sub(r'\bci(\b|$)', "correctional institution", name)
    name = re.sub(r'\bcf(\b|$)', "correctional facility", name)
    return name

facility_lookup = make_facility_lookup("florida", normalize_facility_name)

def search(**kwargs):
    base = "http://www.dc.state.fl.us/ActiveInmates/search.asp"
    search = "http://www.dc.state.fl.us/ActiveInmates/List.asp?DataAction=Filter"
    res = requests.get(base)
    root = lxml.html.fromstring(res.text)
    sessionId = root.xpath("//input[@name='SessionID']/@value")[0]

    res = requests.post(search, {
            "SessionID": sessionId,
            "lastname": kwargs.get('last_name', ''),
            "firstname": kwargs.get('first_name', ''),
            "dcnumber": kwargs.get('number', ''), 
            "searchaliases": "on",
            "race": "ALL",
            "sex": "ALL",
            "eyecolor": "ALL",
            "haircolor": "ALL",
            "fromheightfeet": "",
            "fromheightinches": "",
            "toheightfeet": "",
            "toheightinches": "",
            "fromweight": "",
            "toweight": "",
            "fromage": "",
            "toage": "",
            "offensecategory": "ALL",
            "commitmentcounty": "ALL",
            "facility2": "ALL",
            "items": "20"
        })

    root = lxml.html.fromstring(res.text)
    rows = root.xpath('//table[@class="dcCSStableLight"]//tr')
    results = []
    errors = []
    for row in rows:
        tds = row.xpath('./td')
        if len(tds) != 8:
            continue
        data = {
            "name": "".join(tds[1].xpath('.//text()')).strip(),
            "url": "".join(tds[1].xpath('.//a/@href')).strip(),
            "photo": "".join(tds[0].xpath('.//img/@src')).strip(),
            "dc_number": "".join(tds[2].xpath('.//text()')).strip(),
            "race": "".join(tds[3].xpath('.//text()')).strip(),
            "sex": "".join(tds[4].xpath('.//text()')).strip(),
            "release_date": "".join(tds[5].xpath('.//text()')).strip(),
            "current_facility": "".join(tds[6].xpath('.//text()')).strip(),
            "birth_date": "".join(tds[7].xpath('.//text()')).strip(),
        }
        if data['url']:
            data['url'] = "http://www.dc.state.fl.us/ActiveInmates/" + data['url']
        if data['photo']:
            data['photo'] = "http://www.dc.state.fl.us" + data['photo']
        if data['name']:
            results.append(data)
        else:
            pass
        score, facility = facility_lookup(data['current_facility'])
        if score > 90:
            data['address'] = facility
        else:
            data['address_lookup_failure'] = data['current_facility']

    return {'state': 'Florida', 'results': results, 'errors': list(errors), 'url': base}
