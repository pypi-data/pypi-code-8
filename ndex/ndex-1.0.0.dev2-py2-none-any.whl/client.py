#!/usr/bin/env python

import requests
import json

class Ndex:
        
    def __init__(self, host = "http://www.ndexbio.org", username = None, password = None):
        if "localhost" in host:
            self.host = "http://localhost:8080/ndexbio-rest"
        else:
            self.host = host + "/rest"
        # create a session for this Ndex
        self.s = requests.session()
        if username and password:
            # add credentials to sesson, if available
            self.s.auth = (username, password)
    
# Base methods for making requests to this NDEx
    
    def put(self, route, put_json):
        url = self.host + route  
        print "PUT route: " + url
        print put_json
        headers = {'Content-Type' : 'application/json;charset=UTF-8',
                   'Accept' : 'application/json',
                   'Cache-Control': 'no-cache',
                   }
        response = self.s.put(url, data = put_json, headers = headers)
        response.raise_for_status()
        return response.json()
        
    def post(self, route, post_json):
        url = self.host + route
        print "POST route: " + url
        print post_json
        
        headers = {'Content-Type': 'application/json',
                   'Accept': 'application/json',
                   'Cache-Control': 'no-cache',
                   }
        response = self.s.post(url, data=post_json, headers=headers)
        response.raise_for_status()
        return response.json()
        
    def delete(self, route):
        url = self.host + route
        response = self.s.delete(url)
        response.raise_for_status()
        return response.json()
    
    def get(self, route, get_params = None):
        url = self.host + route
        print "GET route: " + url
        print get_params
        response = self.s.get(url, params = get_params)
        response.raise_for_status()
        return response.json()
        
# Network methods
        

# Search for networks by keywords
#    network    POST    /network/search/{skipBlocks}/{blockSize}    SimpleNetworkQuery    NetworkSummary[]
    def find_networks(self, search_string="", account_name=None, skip_blocks=0, block_size=100):
        route = "/network/search/%s/%s" % (skip_blocks, block_size)
        post_data = {"searchString" : search_string}
        if account_name:
            post_data["accountName"] = account_name
        post_json = json.dumps(post_data)
        return self.post(route, post_json)

    def get_network_api(self):
        route = "/network/api"
        decoded_json = self.get(route)
        return decoded_json
 
#    network    POST    /network/{networkUUID}/edge/asNetwork/{skipBlocks}/{blockSize}        Network
    def get_network_by_edges(self, network_id, skip_blocks=0, block_size=100):
        route = "/network/%s/edge/asNetwork/%s/%s" % (network_id, skip_blocks, block_size)
        return self.get(route)

#    network    GET    /network/{networkUUID}/asNetwork       Network
    def get_complete_network(self, network_id):
        route = "/network/%s/asNetwork" % (network_id)
        return self.get(route)

    def update_network(self, network):
        route = "/network/asNetwork"
        return self.put(route, network)

#    network    GET    /network/{networkUUID}       NetworkSummary
    def get_network_summary(self, network_id):
        route = "/network/%s" % (network_id)
        return self.get(route)
        
#    network    POST    /network    Network    NetworkSummary
    def save_new_network(self, network):
        route = "/network/asNetwork"
        return self.post(route, network)

#    network    POST    /network/asNetwork/group/{group UUID}    Network    NetworkSummary
    def save_new_network_for_group(self, network, group_id):
        route = "/network/asNetwork/group/%s" % (group_id)
        # self.removeUUIDFromNetwork(network)
        return self.post(route, network)
       
##  Neighborhood PathQuery
#    network    POST    /network/{networkUUID}/asPropertyGraph/query    SimplePathQuery    PropertyGraphNetwork    
    def get_neighborhood(self, network_id, search_string, search_depth=1):
        route = "/network/%s/asNetwork/query" % (network_id)
        post_data = {'searchString': search_string,
                   'searchDepth': search_depth}
        post_json = json.dumps(post_data)
        return self.post(route, post_json)