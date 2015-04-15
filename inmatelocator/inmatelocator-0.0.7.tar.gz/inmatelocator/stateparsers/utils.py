import os
import re
import json
from fuzzywuzzy import fuzz
from addresscleaner.us_states import STATES_NORMALIZED

def normalize_name(name):
    name = re.sub("[^-a-z ]", "", name.lower()).strip()
    name = re.sub("-", " ", name)
    name = re.sub("\s+", " ", name)
    return name

def fuzzy_match_address(address, choices):
    scores = []
    for choice in choices:
        score = []
        # Zip handling
        if address.get('state') != choice.get('state'):
            continue
        z1 = address.get('zip').strip()
        z2 = choice.get('zip')
        if z1 and z2:
            score.append(fuzz.partial_ratio(z1, z2))
        # City, org, address
        for key in ["city", "address1", "organization"]:
            v1 = address.get(key)
            v2 = choice.get(key)
            if v1 is not None and v2 is not None:
                v1 = re.sub('[^a-z0-9 ]', '', v1.lower())
                v2 = re.sub('[^a-z0-9 ]', '', v2.lower())
                score.append(fuzz.ratio(v1, v2))
        if score:
            scores.append((sum(score) / float(len(score)), choice))

    if len(scores) == 0:
        return 0, None

    scores.sort()
    return scores[-1][0], scores[-1][1]

def load_data(state_name):
    filename = os.path.join(
        os.path.dirname(__file__),
        "..",
        "data",
        "{}.json".format(state_name))
    with open(filename) as fh:
        data = json.load(fh)
    return data

def make_facility_lookup(state_name, normalize_func=None):
    normalize_func = normalize_func or normalize_name

    facilities = []
    state_data = load_data(state_name)
    for result in state_data:
        facilities.append(result)

    # If we aren't searching federal facilities explicitly, append federal
    # facilities in the current state to our local state results.
    if state_name != "federal":
        federal_data = load_data("federal")
        state = STATES_NORMALIZED[state_name]
        for result in federal_data:
            if result['state'] == state:
                facilities.append(result)

    def lookup(term=None, address=None):
        if term is not None:
            address = {"organization": term}

        if address['organization']:
            address = dict(address.items())
            address['organization'] = normalize_func(address['organization'])

        return fuzzy_match_address(address, facilities)

    return lookup
