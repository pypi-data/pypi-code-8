# slackinviter.py
"""
Accept first name, last name and email address of member
Use the __name__ == '__main__' approach
generate a timestamp for the URL
add the ability to pass credentials (clientid, token, token)
"""
usage = """
usage: 
import autoslack
autoslack.invite(group="SLACKCOMMUNITYNAME",
                token="XXXXXXX",
                firstname="XXXXXXXX",
                lastname="XXXXXXX",
                emailaddress="XXXXXXX",
                channels=['XXXXX','XXXXX'])

"""

import requests
import time

def invite(group="",
                token="",
                firstname="",
                lastname="",
                emailaddress="",
                channels=[]):

    timestamp=int(time.time())
    slackuserapi = "api/users.admin.invite"
    url = "https://{}.slack.com/{}?t={}".format(
                                               group,
                                               slackuserapi,
                                               timestamp
                                               )
    # we should consider the channel api to autoinvite users to all channels

    channels = ",".join(channels)
    payload = {}
    payload["email"]=emailaddress
    payload["channels"]=channels
    payload["first_name"]=firstname
    payload["last_name"]=lastname
    payload["token"]=token
    payload["set_active"]="true"
    payload["_attempts"]=1
    
    
    r = requests.post(
                   url,
                   data=payload
#                   auth=(clientid,secret)
                   )
    # the print statements are here for the sake of debugging
    return r.json()

if __name__ == '__main__':
    
    print("use this module with another program")
    print(usage)
    print ("# that is all!")
    
