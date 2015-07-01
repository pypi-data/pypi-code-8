#!/usr/bin/env python

import requests
import json

class Ndex:
        
    def __init__(self, host = "http://www.ndexbio.org", username = None, password = None):
        self.debug = False
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

    def set_debug_mode(self, debug):
        self.debug = debug

    
    def put(self, route, put_json):
        url = self.host + route
        if self.debug:
            print "PUT route: " + url
        headers = {'Content-Type' : 'application/json;charset=UTF-8',
                   'Accept' : 'application/json',
                   'Cache-Control': 'no-cache',
                   }
        response = self.s.put(url, data = put_json, headers = headers)
        response.raise_for_status()
        if response.status_code == 204:
            return ""
        return response.json()
        
    def post(self, route, post_json):
        url = self.host + route
        if self.debug:
            print "POST route: " + url
        headers = {'Content-Type': 'application/json',
                   'Accept': 'application/json',
                   'Cache-Control': 'no-cache',
                   }
        response = self.s.post(url, data=post_json, headers=headers)
        response.raise_for_status()
        if response.status_code == 204:
            return ""
        return response.json()
        
    def delete(self, route):
        url = self.host + route
        if self.debug:
            print "DELETE route: " + url
        response = self.s.delete(url)
        response.raise_for_status()
        if response.status_code == 204:
            return ""
        return response.json()
    
    def get(self, route, get_params = None):
        url = self.host + route
        if self.debug:
            print "GET route: " + url
        response = self.s.get(url, params = get_params)
        response.raise_for_status()
        if response.status_code == 204:
            return ""
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
        if isinstance(network, dict):
            putJson = json.dumps(network)
        else:
            putJson = network
        return self.put(route, putJson)

#    network    GET    /network/{networkUUID}       NetworkSummary
    def get_network_summary(self, network_id):
        route = "/network/%s" % (network_id)
        return self.get(route)
        
#    network    POST    /network    Network    NetworkSummary
    def save_new_network(self, network):
        route = "/network/asNetwork"
        if isinstance(network, dict):
            postJson = json.dumps(network)
        else:
            postJson = network
        return self.post(route, postJson)

#    network    POST    /network/asNetwork/group/{group UUID}    Network    NetworkSummary
    def save_new_network_for_group(self, network, group_id):
        route = "/network/asNetwork/group/%s" % (group_id)
        # self.removeUUIDFromNetwork(network)
        return self.post(route, network)

    def delete_network(self, network_id):
        route = "/network/%s" % (network_id)
        return self.delete(route)

    def get_neighborhood(self, network_id, search_string, search_depth=1):
        route = "/network/%s/asNetwork/query" % (network_id)
        post_data = {'searchString': search_string,
                   'searchDepth': search_depth}
        post_json = json.dumps(post_data)
        return self.post(route, post_json)

    def get_provenance(self, network_id):
        route = "/network/%s/provenance" % (network_id)
        return self.get(route)

    def set_provenance(self, network_id, provenance):
        route = "/network/%s/provenance" % (network_id)
        if isinstance(provenance, dict):
            putJson = json.dumps(provenance)
        else:
            putJson = provenance
        return self.put(route, putJson)

    def set_network_flag(self, network_id, parameter, value):
        route = "/network/%s/setFlag/%s=%s" % (network_id, parameter, value)
        return self.get(route)

    def set_read_only(self, network_id, value):
        return self.set_network_flag(network_id, "readOnly", value)

    def set_network_properties(self, network_id, network_properties):
        route = "/network/%s/properties" % (network_id)
        if isinstance(network_properties, list):
            putJson = json.dumps(network_properties)
        else:
            putJson = network_properties
        return self.put(route, putJson)

    def update_network_profile(self, network_id, network_profile):
        route = "/network/%s/summary" % (network_id)
        if isinstance(network_profile, dict):
            postJson = json.dumps(network_profile)
        else:
            postJson = network_profile
        return self.post(route, postJson)

    def search_for_networks_by_network_properties(self, query):
        route = "/network/searchByProperties"
        if isinstance(query, dict):
            postJson = json.dumps(query)
        else:
            postJson = query
        return self.post(route, postJson)