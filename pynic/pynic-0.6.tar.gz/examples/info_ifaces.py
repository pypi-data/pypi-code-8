#!/usr/bin/python

# Author: Alfredo Miranda
# E-mail: alfredocdmiranda@gmail.com
# Date: 03/01/2015
#
# This is a sample code to pyIface, which lists NICs on computer and 
# show information about them.

import pynic

list_interfaces = pynic.get_list_interfaces()

for pos, i in enumerate(list_interfaces):
    print("{0} - {1}".format(pos, i))

opt = int(input("Choose the interface: "))

print("########## Interface Info ##########")
iface = pynic.Iface.get_interface(list_interfaces[opt])

print("Name: {0}".format(iface.name))
print("IPv4: {0}".format(iface.inet_addr))
print("IPv6: {0}".format(iface.inet6_addr))
print("MAC: {0}".format(iface.hw_addr))
print("Broadcast: {0}".format(iface.broad_addr))
print("Netmask: {0}".format(iface.inet_mask))
print("Netmask v6: {0}".format(iface.inet6_mask))
print("Running: {0}".format(iface.running))
print("Up: {0}".format(iface.updown))
print("TX bytes: {0} bytes".format(iface.tx_bytes))
print("RX bytes: {0} bytes".format(iface.rx_bytes))
print("TX packets: {0} packets".format(iface.tx_packets))
print("RX packets: {0} packets".format(iface.rx_packets))
