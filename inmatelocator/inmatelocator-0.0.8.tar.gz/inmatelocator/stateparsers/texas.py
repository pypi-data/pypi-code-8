import re
import requests
from inmatelocator.utils import normalize_name, texas_unit_type_re, make_facility_lookup
import lxml.html

facility_name_overrides = {
    'carol young complex': 'Carole S. Young Medical Facility',
    'diboll priv': 'Diboll Correctional Center',
    'east texas treatment facility': 'East Texas Multi-Use Facility',
    'hospital galv': 'Hospital Galveston',
    'jester i': 'Beauford H. Jester I Unit',
    'jester ii': 'Beauford H. Jester II Unit',
    'jester iii': 'Beauford H. Jester III Unit',
    'jester iv': 'Beauford H. Jester IV Unit',
    'lockhart work fac': 'Lockhart Correctional Facility',
    'pack i': 'Wallace Pack Unit',
    'ramsey i': 'W. F. Ramsey Unit',
    'west texas isf': 'West Texas Intermediate Sanction Facility',
    'west texas hosp': 'West Texas Intermediate Sanction Facility',
}

def normalize_texas_name(name):
    name = normalize_name(name)
    if name in facility_name_overrides:
        return normalize_name(facility_name_overrides[name])
    return name 

facility_lookup = make_facility_lookup("texas", normalize_texas_name)

def search(**kwargs):
    url = "http://offender.tdcj.state.tx.us/OffenderSearch/search.action"

    # Fix number formatting
    number = kwargs.get('number', '')
    if number:
        number_types = ("tdcj", "sid")
        number = re.sub('[^0-9]', '', number)
        number = "0" * (8 - len(number)) + number
    else:
        number_types = ("sid")

    results = []
    errors = []

    for number_type in number_types:
        params = {
            "page": "index",
            "lastName": kwargs.get('last_name', ''),
            "firstName": kwargs.get('first_name', ''),
            "gender": "ALL",
            "race": "ALL",
            "btnSearch": "Search",
        }
        params[number_type] = number
        res = requests.post(url, params)

        root = lxml.html.fromstring(res.text)
        rows = root.xpath('//table[@class="ws"]//tr')
        for row in rows:
            data = {
                'name': "".join(row.xpath('./td[1]/a/text()')),
                'url': "http://offender.tdcj.state.tx.us" + "".join(row.xpath('./td[1]/a/@href')),
                'tdcj_number': "".join(row.xpath('./td[2]/text()')),
                'race': "".join(row.xpath('./td[3]/text()')),
                'gender': "".join(row.xpath('./td[4]/text()')),
                'projected_release_date': "".join(row.xpath('./td[5]/text()')),
                'unit_of_assignment': "".join(row.xpath('./td[6]/text()')),
                'date_of_birth': "".join(row.xpath('./td[7]/text()')),
            }
            try:
                data['sid_number'] = data['url'].split("sid=")[1]
            except (KeyError, IndexError):
                pass
            if data['unit_of_assignment']:
                score, address = facility_lookup(term=data['unit_of_assignment'])
                if score > 90:
                    data['address'] = address
                else:
                    data['address_lookup_failure'] = data['unit_of_assignment']

            if data['url']:
                match = re.search("sid=([-0-9a-zA-Z]+)", data['url'])
                if match:
                    data['sid_number'] = match.group(1)
            if data['name']:
                results.append(data)
            else:
                pass
                #errors.append(''.join(row.xpath('.//text()')))
        if results:
            break
    return {'state': 'Texas', 'results': results, 'errors': list(errors), 'url': url}
