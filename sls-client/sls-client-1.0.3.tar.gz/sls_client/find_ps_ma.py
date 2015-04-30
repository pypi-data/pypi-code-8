__author__ = 'sowmya'

from sls_client.records import *
from sls_client.query import *
import sys
import json
import socket

from optparse import OptionParser

def get_ma_for_host(hostname):

    ipaddresses={}
    if(not hostname):
        raise Exception("Null Parameter", "Hostname parameter is empty.")
    ipaddr = socket.getaddrinfo(hostname, None)

    #ipaddr is a 5-tuple and the ipv4 or ipv6 is the last element in the tuple.
    for ip in ipaddr:
        if(ip[4][0]):
            ipaddresses[ip[4][0]]=1

    response=[]
    result={}
    queryKeys = ['psmetadata-dst-address','psmetadata-src-address']
    for queryKey in queryKeys:
        queryString=""
        for ip in ipaddresses:
            queryString += queryKey+"="+ip+"&"
        response += query(queryString)


    for record in response:
        malocators = record[u'psmetadata-ma-locator']
        for malocator in malocators:
            malocatorString = malocator.encode("ascii")
            result[malocatorString] = 1

    return result.keys()

def get_json(query,hostlist):
    result={}
    result["ma-hosts"] = []
    result["search-query"] = query
    if(hostlist):
        result["ma-hosts"] = hostlist

    json_output = json.dumps(result)
    return json_output


def main():

    parser = OptionParser()

    parser.add_option("-n", "--hostname",
                      dest="hostname",
                      help="specify hostname or IP")
    parser.add_option("-o", "--output",
                      dest="output_type",
                      help="output type - json or console",
                      choices=["console","json"],
                      default="console"
                      )
    (options, args) = parser.parse_args()

    if (not options.hostname):
        print "Please specify hostname"
        sys.exit(1)

    result = get_ma_for_host(options.hostname)
    if(options.output_type == "json"):
        output=get_json(options.hostname,result)
        print output
    else:
        for host in result:
            print host
if __name__=='__main__':
    main()