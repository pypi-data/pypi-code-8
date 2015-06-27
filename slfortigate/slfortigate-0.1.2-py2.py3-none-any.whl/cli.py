#!/usr/bin/env python2
# -*- coding: latin-1 -*-
""" Order and configure fortigate security appliance in softlayer.
For examples of invoking this script, see the help info below.

    TODO:
    - use logger
    - stop swallowing exceptions
    - use function composition to abstract out repeated exec-and-wait loop structures
"""

__author__ = 'Bruce Potter <bp@us.ibm.com>'
__copyright__ = '2015 IBM'
__license__ = 'EPL-1.0'

import SoftLayer
import sys
import os
import json
import pprint
import re
import argparse
import time
import datetime
from slfortigate import configure
from SoftLayer.exceptions import SoftLayerAPIError, SoftLayerError, Unauthenticated

# TESTMODE = False

def verifyPermissions(client, permissions):
    '''Get the list of permissions for the softlayer user authenticated to this API and return any specified permissions the user does not have.'''
    try:
        user = client['Account'].getCurrentUser(mask='id, username, permissions, account.id, account.masterUser.username, account.masterUser.permissions')
        # This is a SL idiosyncrasy that they return an empty list for the permissions of the master user. They also do not return account for the master user.
        # Add if this is a non-master user w/o the USER_MANAGE permission, they can not see the masterUser info.
        if 'account' not in user or ('masterUser' in user['account'] and user['username']==user['account']['masterUser']['username']):  return []

        # build a set with both the keyNames and names (so we can check them both)
        pset = set()
        for p in user['permissions']:
            pset.add(p['keyName'])
            pset.add(p['name'])

        # Compare the required permissions with the actual list in pset
        perms = {}
        unmet = []
        for p in permissions:
            if p not in pset:
                unmet.append(p)
        return unmet
    except SoftLayerAPIError as e:
        slError(e)

def getDataCenters(client):
    '''Return the list of short dc names as a set.'''
    datacenters = client['Location'].getDataCenters(mask='name')
    # datacenters = client['Location_Datacenter'].getDataCenters()
    dset = set()
    for d in datacenters:
        dset.add(d['name'])
    return dset

def getPublicVlans(client, dc):
    '''Find all existing public vlans in this dc that are not transit vlans.'''
    mask = 'id, vlanNumber, attachedNetworkGatewayFlag, dedicatedFirewallFlag, networkSpace, type.id, primaryRouter.hostname, primaryRouter.datacenterName, primaryRouter.datacenter.name'
    filt = {'networkVlans': {
        'networkSpace': {'operation': 'PUBLIC'},
        # 'attachedNetworkGatewayFlag': {'operation': 0},     # this check makes the call take 5 times longer
        # 'dedicatedFirewallFlag': {'operation': 0},     # this check makes the call take 5 times longer
        'primaryRouter': {'datacenter': {'name': {'operation': dc} } },
        'type': {'id': {'operation': 1} },      # this means regular vlan, type.id==2 is a transit vlan
        } }
    vlans = client['Account'].getNetworkVlans(mask=mask, filter=filt)
    return vlans

    # filter out vlans with attachedNetworkGatewayFlag==True or dedicatedFirewallFlag==1
    # vlans2 = []
    # for v in vlans:
    #     if not v['attachedNetworkGatewayFlag'] and not v['dedicatedFirewallFlag']:  vlans2.append(v)
    # return vlans2

def orderSimpleVsi(client, dc, reallyOrder):
    '''Use the simplified form of ordering a vsi, but just verify the order.'''
    # Reference: http://sldn.softlayer.com/reference/services/SoftLayer_Virtual_Guest/createObject/
    global TESTMODE
    if TESTMODE:
        vsiObj = {'id':10259907, 'hostname':'fgdummyvsi', 'domain': 'feat.com', 'fullyQualifiedDomainName': 'fgdummyvsi.feat.com'}
        return vsiObj
    vsi = {
        'datacenter': {'name': dc},
        'hostname': 'fgdummyvsi',
        'domain': 'feat.com',
        'hourlyBillingFlag': True,
        "startCpus": 1,
        "maxMemory": 1024,
        "localDiskFlag": True,
        'blockDevices': [{'device': '0', 'diskImage': {'capacity': 25}}],
        'networkComponents': [{'maxSpeed': 100}],
        # 'privateNetworkOnlyFlag': True,
        # 'primaryNetworkComponent': { 'networkVlan': {'id': 123456} },
        # 'primaryBackendNetworkComponent': { 'networkVlan': {'id': 567890} },
        'operatingSystemReferenceCode': 'UBUNTU_LATEST',
        # 'userData': [{'value': 'stuff'}],
        # 'sshKeys': [{'id': 123456}],        # use client['Account'].getSshKeys() to get the id's of the ssh keys
        # 'postInstallScriptUri': 'script-name',
    }

    try:
        if not reallyOrder:
            # this just verifies the order
            productOrder = client['Virtual_Guest'].generateOrderTemplate(vsi)
            order = client['Product_Order'].verifyOrder(productOrder)
            return order
        else:
            # to really order:
            vsiObj = client['Virtual_Guest'].createObject(vsi)
            return vsiObj
    except SoftLayerAPIError as e:
        slError(e)

def getVsiVlan(client, vsiObj, waitTime):
    '''Wait for vsi to be provisioned enough to return the public vlan this vsi is on.'''
    vsiId = vsiObj['id']
    pollInterval = 10       # seconds
    numberOfChecks = 6 * int(waitTime)           # we will check every 10 seconds
    try:
        for i in range(numberOfChecks):
            mask = 'id, provisionDate, activeTransactions, primaryNetworkComponent.id, primaryNetworkComponent.networkVlan.id, primaryNetworkComponent.networkVlan.vlanNumber, primaryNetworkComponent.networkVlan.primaryRouter.hostname'
            vsi = client['Virtual_Guest'].getObject(id=vsiId, mask=mask)
            if 'primaryNetworkComponent' in vsi and 'networkVlan' in vsi['primaryNetworkComponent'] and 'id' in vsi['primaryNetworkComponent']['networkVlan']:
                vName = str(vsi['primaryNetworkComponent']['networkVlan']['vlanNumber']) + '.' + vsi['primaryNetworkComponent']['networkVlan']['primaryRouter']['hostname']
                # if TESTMODE:  return 1234567, '1234.fcr01a.tor01'        # our fg is on this vlan
                # else:
                return vsi['primaryNetworkComponent']['networkVlan']['id'], vName
            # vsi not ready, print msg and try again

            print(' VSI not ready yet, activeTransactions: {}, provisionDate: {}'.format(vsi['activeTransactions'], vsi['provisionDate']))
            time.sleep(pollInterval)
        return None, None
    except SoftLayerAPIError as e:
        slError(e)

def deleteVsi(client, vsiId):
    global TESTMODE
    try:
        if not TESTMODE:
            result = client['Virtual_Guest'].deleteObject(id=vsiId)
    except SoftLayerAPIError as e:
        slError(e)

def verifyExistingVlan(client, vlan):
    '''Get info about this vlan so we can verify it.'''
    mask = 'id, vlanNumber, attachedNetworkGatewayFlag, dedicatedFirewallFlag, networkSpace, type.id, primaryRouter.hostname'
    vlanNum, router = vlan.split('.', 1)
    filt = {'networkVlans': {'vlanNumber': {'operation': vlanNum}, 'primaryRouter': {'hostname': {'operation': router} } }}
    try:
        vlans = client['Account'].getNetworkVlans(mask=mask, filter=filt)
        if not vlans or len(vlans)!=1:  error(2, 'VLAN '+vlan+' does not exist in this SoftLayer account')
        if vlans[0]['type']['id'] == 2:  error(2, 'VLAN '+vlan+' is a vyatta transit VLAN, it can not be protected by a Fortigate appliance.')
        if vlans[0]['attachedNetworkGatewayFlag']:  error(2, 'VLAN '+vlan+' is already associated to a vyatta gateway.')
        if vlans[0]['dedicatedFirewallFlag'] != 0:  error(2, 'VLAN '+vlan+' is already protected by a firewall.')
        if vlans[0]['networkSpace'] != 'PUBLIC':  error(2, 'VLAN '+vlan+' is not a public VLAN')
        return vlans[0]['id']
    except SoftLayerAPIError as e:
        slError(e)

def orderFortigate(client, vlanId, reallyOrder, verbose=False):
    # get the location of the vlan
    global TESTMODE
    mask = 'id, vlanNumber, primaryRouter.hostname, primaryRouter.datacenter.id'
    vlan = client['Network_Vlan'].getObject(id=vlanId, mask=mask)
    locationId = vlan['primaryRouter']['datacenter']['id']

    if verbose:
        print('locationId: {}'.format(locationId))

    if TESTMODE:
        return {'foo':'bar'}

    productOrder = {
        'complexType': 'SoftLayer_Container_Product_Order_Network_Protection_Firewall_Dedicated',
        'vlanId': vlanId,
        'location': locationId,
        'packageId': 0,
        'prices': [{'id': 21514}],   # FORTIGATE_SECURITY_APPLIANCE
        'quantity': 1,
    }

    try:
        if not reallyOrder:
            order = client['Product_Order'].verifyOrder(productOrder)
        else:
            order = client['Product_Order'].placeOrder(productOrder, False)
        return order
    except SoftLayerAPIError as e:
        slError(e)

def getFortigateInfo(client, fgName, waitTime, vlanId=0, verbose=False):
    '''Wait for the fortigate to be provisioned, and then return ip, user, pw.'''

    pollInterval = 10       # seconds
    numberOfChecks = 6 * int(waitTime)           # we will check every 10 seconds
    try:
        for i in range(numberOfChecks):
            mask = 'id, vlanNumber, primaryRouter.hostname, dedicatedFirewallFlag, \
                    networkVlanFirewall.customerManagedFlag, networkVlanFirewall.networkFirewallUpdateRequests, networkVlanFirewall.administrativeBypassFlag, \
                    networkVlanFirewall.managementCredentials.username, networkVlanFirewall.managementCredentials.password, networkVlanFirewall.fullyQualifiedDomainName, networkVlanFirewall.primaryIpAddress'
            if vlanId:
                vlan = client['Network_Vlan'].getObject(id=vlanId, mask=mask)
            else:
                # need to figure out how to find the firewall by hostname, but for now pull the vlan num out of the hostname
                # the fg hostname is like:  firewall-vlan1234.networklayer.com
                match = re.search(r"^firewall-vlan(\d+)(\.|$)", fgName)
                if not match:  error(2, 'Fortigate hostname '+fgName+' is not in the format expected')
                vlanNum = int(match.group(1))
                filt = {'networkVlans': {'vlanNumber': {'operation': vlanNum} }}
                vlans = client['Account'].getNetworkVlans(mask=mask, filter=filt)
                if not vlans:  errors(2, 'can not find fortigate '+fgName)
                elif len(vlans)>1:  errors(2, 'more than 1 vlan with number '+str(vlanNum))
                vlan = vlans[0]

            if verbose:  pprint.pprint(vlan)

            if 'networkVlanFirewall' in vlan:
                fg = vlan['networkVlanFirewall']

                if ('fullyQualifiedDomainName' in fg and fg['fullyQualifiedDomainName'].startswith(fgName)
                        and 'primaryIpAddress' in fg
                        and 'managementCredentials' in fg
                        and 'username' in fg['managementCredentials'] and fg['managementCredentials']['username']
                        and 'password' in fg['managementCredentials'] and fg['managementCredentials']['password']
                        and 'vlanNumber' in vlan and 'primaryRouter' in vlan and 'hostname' in vlan['primaryRouter']):

                    return fg['primaryIpAddress'], '{}.{}'.format(vlan['vlanNumber'], vlan['primaryRouter']['hostname']), fg['managementCredentials']['username'], fg['managementCredentials']['password']

            # fg not ready, print msg and try again
            print(' Fortigate {} not ready yet, still waiting...'.format(fgName))
            time.sleep(pollInterval)
        return None, None, None, None
    except SoftLayerAPIError as e:
        slError(e)

def writeOrderToFile(order, filename):
    '''put order quote in output file'''
    f = open(filename, 'w')
    # f.write(str(order))
    pprint.pprint(order, f)
    f.close()
    return

def error(code, msg):
    '''Print the error msg and exit with code. Barf out stacktrace. '''

    print('Error: {}'.format(msg))
    sys.exit(code)

def slError(slException):
    '''Handle the common cases with SL exceptions and return the appropriate msg.'''

    error(1, '{}: {}'.format(slException.faultCode, slException.faultString))

def main():
    # parse cmd line args
    parser = argparse.ArgumentParser(formatter_class=argparse.RawDescriptionHelpFormatter,
        description='''Order and configure a fortigate security appliance, locking down the vlan by default, so that all subsequent
    servers ordered on this vlan will be protected immediately.''',
        epilog='''In addition to the options below, you also need to set environment variables
    SL_USERNAME and SL_API_KEY, or have them in your ~/.softlayer file.

    EXAMPLES:

    # Order a fortigate security appliance in a new datacenter:
    slfortigate -d tor01 --output ~/tmp/order.txt --really-order

    # Order a fortigate security appliance on a specific VLAN:
    slfortigate --vlan 1275.fcr01a.tor01 --output ~/tmp/order.txt --really-order

    # Configure an existing fortigate security appliance:
    slfortigate --config-existing firewall-vlan1729.networklayer.com
    ''')
    # parser.add_argument('vyatta', metavar='gatewayname',
    #     help='The name of the gateway. If it is a gateway appliance, specify the short name.  If it is a gateway virtual server, specify the fully qualified domain name.')
    parser.add_argument('-d', '--datacenter', metavar='datacenter', required=False,
        help='the datacenter to create this fortigate in. Use the short name of the datacenter, e.g. sjc01. Use this option instead of --vlan when you do not have any servers in this datacenter yet. A small VSI will automatically be created to get a public vlan and the fortigate put on that vlan.')
    parser.add_argument('--vlan', metavar='protectedvlan', required=False,
        help='the existing VLAN to be protected by the fortigate, specified as <vlanNum>.<routerHostname>, for example, 1738.fcr01a.tor01. Either this argument or --datacenter must be specified.')
    parser.add_argument('--ha-pair', action="store_true",
        help="not yet implemented! You want to order 2 fortigates configured together as an HA pair")
    parser.add_argument('-o', '--output', metavar='file',
        help="file name to put the order or quote output in, instead of displaying it to stdout. The order/quote data structure is very large, so you will probably want it in a file.")
    parser.add_argument('--really-order', action="store_true",
        help="really order the fortigate, otherwise just get a quote")
    parser.add_argument('--config-existing', metavar='hostname',
        help="the hostname of an existing fortigate to configure instead of ordering a new fortigate")
    parser.add_argument('-v', "--verbose", action="store_true",
        help="display verbose output")

    # Check input
    global TESTMODE
    if 'FG_TEST_MODE' in os.environ and os.environ['FG_TEST_MODE']:  TESTMODE = True
    else:  TESTMODE = False
    args = parser.parse_args()
    # pprint.pprint(args)
    if not args.config_existing and not (args.datacenter or args.vlan):  error(2, 'must specify either --datacenter or --vlan')
    if args.config_existing and (args.datacenter or args.output or args.really_order):  error(2, 'can not specify --config-existing with --datacenter or --output or --really-order')
    if args.vlan and args.vlan.find('.') == -1:  error(2, 'VLAN '+args.vlan+' must have the router hostname appended to make it unique.')

    # username and api_key come from sl env vars or .softlayer file
    # client = SoftLayer.Client(username=myuser, api_key=mykey, endpoint_url=SoftLayer.API_PUBLIC_ENDPOINT)
    client = SoftLayer.Client(endpoint_url=SoftLayer.API_PUBLIC_ENDPOINT)

    print 'Checking permissions...'
    # make sure they have the SL permissions needed to complete the task.  This will also kick out
    # if they do not have a valid SL username and api key.
    requiredPermissions = ['Hardware Firewall', 'add server']
    response = verifyPermissions(client, requiredPermissions)
    if response:
        error(2, 'you need the following SoftLayer permissions to order and configure the fortigate:'+', '.join(response)+" To add the missiing permissions, go to https://gateway-as-a-service.com/gaas/v1/spec.html#!/spec/user_permissions_put, enter your SoftLayer parent's username and API key, your username, and the list of permissions, and then click 'Try it out'.")

    if args.datacenter:
        # verify specified datacenter
        datacenters = getDataCenters(client)
        if args.datacenter not in datacenters:  error(2, args.datacenter+' is not a valid SoftLayer datacenter name. Valid choices are: '+', '.join(datacenters))

        # Check for existing public vlans in this dc, 4 cases:
        # - no public vlans:  order a dummy vsi to create one
        # - at least 1 public vlan, but they are all protected:  error msg that if they want an additional vlan, have to use --vlan arg
        # - only 1 unprotected public vlan:  protect that with the fortigate, do not need to order a dummy vsi
        # - more than 1 unprotected vlan:  error msg that they need to specify which one with --vlan arg
        print 'Checking existing VLANs in '+args.datacenter+'...'
        needToOrderDummyVsi = False
        vlans = getPublicVlans(client, args.datacenter)
        if not vlans or TESTMODE:
            needToOrderDummyVsi = True
        else:
            # there is at least 1 vlan in this dc, handle the other 3 cases
            # find the unprotected vlans by filtering out the already protected vlans that have attachedNetworkGatewayFlag==True or dedicatedFirewallFlag==1
            unprotectedVlans = []
            for v in vlans:
                if not v['attachedNetworkGatewayFlag'] and not v['dedicatedFirewallFlag']:  unprotectedVlans.append(v)
            if not unprotectedVlans:
                # all existing vlans are already protected by a fortigate or vyatta
                vlanNames = []
                for v in vlans:
                    vlanNames.append(str(v['vlanNumber'])+'.'+v['primaryRouter']['hostname'])
                error(2, 'all existing VLANs in datacenter '+args.datacenter+' ('+', '.join(vlanNames)+') already have a Fortigate or Vyatta appliance protecting them. If you want to protect an additional VLAN in this datacenter with a Fortigate appliance, create the VLAN and then run this command again with the --vlan argument.')
            elif len(unprotectedVlans) == 1:
                # we will put the fortigate on this vlan, but do not need to create a dummy vsi
                needToOrderDummyVsi = False
                v = unprotectedVlans[0]
                if TESTMODE:
                    vlanId = 881101
                    vlanName = '1729.fcr01a.tor01'
                else:
                    vlanId = v['id']
                    vlanName = str(v['vlanNumber'])+'.'+v['primaryRouter']['hostname']
            else:
                # more than 1 unprotected vlan in this dc, they have to tell us which one to protect
                uVlanNames = []
                for v in unprotectedVlans:
                    uVlanNames.append(str(v['vlanNumber'])+'.'+v['primaryRouter']['hostname'])
                error(2, 'there are multiple unprotected VLANs in datacenter '+args.datacenter+' ('+', '.join(uVlanNames)+').  Use the --vlan argument to specify which one you want protected with a new Fortigate appliance.')

        if needToOrderDummyVsi:
            # order vsi
            print('Ordering a temporary small hourly VSI to get public VLAN...')
            vsiObj = orderSimpleVsi(client, args.datacenter, args.really_order)
            if not args.really_order:
                if args.output:
                    writeOrderToFile(vsiObj, args.output)
                else:
                    pprint.pprint(vsiObj)
                print('Did not actually order the VSI because --really-order was not specified')
                sys.exit()      # can not continue if we did not really order the vsi

            if args.verbose:
                pprint.pprint(vsiObj)

            # get the public vlan of the vsi
            waitTime = 10       # minutes
            print('Waiting for VSI to be provisioned (up to {} minutes)...'.format(waitTime))
            vlanId, vlanName = getVsiVlan(client, vsiObj, waitTime)
            if not vlanId:  error(2, 'could not get VLAN from the small VSI we provisioned ('+vsiObj['fullyQualifiedDomainName']+')')

            if args.verbose:
                print('vlanId: {} vlanName: {}'.format(vlanId, vlanName))

    if args.vlan:
        print('Verifying VLAN...')
        vlanName = args.vlan
        vlanId = verifyExistingVlan(client, vlanName)
        if TESTMODE:
            vlanName = '1729.fcr01a.tor01'
            vlanId = 881101

    if not args.config_existing:
        print('Ordering Fortigate Security Appliance to protect vlan {}...'.format(vlanName))
        order = orderFortigate(client, vlanId, args.really_order, args.verbose)
        if args.output:
            writeOrderToFile(order, args.output)
        else:
            pprint.pprint(order)
        if not args.really_order:  sys.exit()


    waitTime = 10       # minutes
    print('Waiting for the Fortigate to be provisioned (up to {} minutes)...'.format(waitTime))
    if args.config_existing:
        fgName = args.config_existing
        vlanId = 0
    else:
        vlanNum, router = vlanName.split('.', 1)
        fgName = 'firewall-vlan'+vlanNum+'.networklayer.com'

    ip, vlanName, user, pw = getFortigateInfo(client, fgName, waitTime, vlanId=vlanId, verbose=args.verbose)         # this also waits for the fg to be provisioned

    if args.verbose:
        print('ip: {}, user: {}, pw: {}'.format(ip, user, pw))

    print('Configuring Fortigate {} to lock down the VLAN'.format(fgName))
    cf = configure.ConfigureFortigate(user, pw, ip, verbose=args.verbose)
    # It seems like the fortigate rules get defined in a post provisioning script that does not finish running until after the
    # fortigate returns a login user/pw, so we have to loop to make sure we get all the rules.
    if args.config_existing:
        rc, msg = cf.denyAllUserTraffic()
        if rc > 1:  error(rc, msg)      # something bad happened
        # both rc 0 and 1 are ok
        if args.verbose and msg:  print(str(msg))
        successfullyConfigured = True
    else:
        # configuring a new fortigate
        pollInterval = 3
        numberOfChecks = 10
        deletedSomePolicies = False
        successfullyConfigured = False
        for i in range(numberOfChecks):
            time.sleep(pollInterval)        # sleep at the beginning to give it a chance to finish the provisioning
            rc, msg = cf.denyAllUserTraffic()
            if rc > 1:
                if args.datacenter and needToOrderDummyVsi:
                    print('Deleting the temporary VSI...')
                    deleteVsi(client, vsiObj['id'])
                error(rc, msg)      # something bad happened
            if args.verbose and msg:  print(str(msg))
            if rc == 0:
                # we successfully deleted some rules, keep going until there are no rules to delete
                deletedSomePolicies = True
                print('Successfully deleted some policies, looking for more...')
            elif rc == 1:
                # there were no policies to delete this time
                if deletedSomePolicies:
                    # we deleted some policies and then there were none to delete.  Consider this success
                    successfullyConfigured = True
                    break
                else:
                    # we caught it before the policies were created, so keep trying...
                    print('Did not find any policies to delete yet, still looking...')

        # if args.datacenter:
        #     print('Deleting the temporary VSI...')
        #     deleteVsi(client, vsiObj['id'])

    if args.datacenter and needToOrderDummyVsi:
        print('Deleting the temporary VSI...')
        deleteVsi(client, vsiObj['id'])

    if successfullyConfigured:
        print('Fortigate {} ({}) now has VLAN {} locked down.'.format(fgName, ip, vlanName))
        sys.exit()
    else:
        error(2, 'could not find policies to delete on the Fortigate appliance.')
    sys.exit()

if __name__ == '__main__':
    main()

# vim: set ts=4 sw=4 expandtab:
