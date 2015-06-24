import json
from .Query import Query
from .DBManager import DBManager


def load_qms_config(file_name):
    f = None
    try:
        f = open(file_name, 'r')
    except:
        print("Missing "+file_name)

    if f is not None:
        parsed = json.loads(f.read())
        for name in parsed:
            DBManager.set(name, parsed[name]['handler'], parsed[name]['parameters'])