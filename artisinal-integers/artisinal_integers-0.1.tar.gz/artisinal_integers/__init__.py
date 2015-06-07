import requests
from random import randint

#######################################

def create(provider=0):

    if (provider == "mission"):
        artisinal_int = create_mission_integer()
    elif (provider == "brooklyn"):
        artisinal_int = create_brooklyn_integer()
    else:
        provider = randint(0,1)
        if (provider == 0):
            artisinal_int = create_mission_integer()
        else:
            artisinal_int = create_brooklyn_integer()
            
    return artisinal_int

#######################################

def create_brooklyn_integer():

    payload = {'method': 'brooklyn.integers.create'}
    r = requests.post("http://api.brooklynintegers.com/rest", data=payload)
    
    return r.text
    

#######################################

def create_mission_integer():

    payload = {'format': 'text'}
    r = requests.post("http://www.missionintegers.com/next-int", data=payload)
    return r.text
