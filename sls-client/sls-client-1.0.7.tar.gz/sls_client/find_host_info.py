__author__ = 'sowmya'

from sls_client.records import *
from sls_client.query import *
import json
import socket


def get_host_info(hostname):
    if(not hostname):
        raise Exception("Null Parameter", "Hostname parameter is empty.")

    ipaddr = socket.getaddrinfo(hostname, None)
    ipaddresses={}
    #ipaddr is a 5-tuple and the ipv4 or ipv6 is the last element in the tuple.
    for ip in ipaddr:
        if(ip[4][0]):
            ipaddresses[ip[4][0]]=1
    response=[]
    queryKey = 'interface-addresses'

    ipaddresses[hostname]=1
    for ip in ipaddresses:
        queryString = queryKey+"="+ip
        response += query(queryString)

    uris=[]
    for record in response:
        uris.append(record[u'uri'])

    hostQueryKey='host-net-interfaces'
    hostResponse=[]
    for uri in uris:
        hostQuery=hostQueryKey+"="+uri
        hostResponse += query(hostQuery)

    for host in hostResponse:
        host[hostQueryKey]=ipaddresses

    return hostResponse

def get_host_info_json(hostname):
    hostlist = get_host_info(hostname)
    result={}
    result["host"] = []
    result["search-query"] = hostname
    if(hostlist):
        result["host"] = hostlist

    json_output = json.dumps(result)
    return json_output
