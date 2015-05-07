#!/usr/bin/python

# Author: Alfredo Miranda
# E-mail: alfredocdmiranda@gmail.com
# Date: 04/24/2015
#
# This is a sample code to pyNIC, which lists NICs on computer and 
# ask a new IPv4 Address to be set. You must have root permission.

import pynic

#Compatible code between Python 2.x and 3.x
try:
    input = raw_input
except NameError:
    pass

list_interfaces = pynic.get_list_interfaces()

for pos, i in enumerate(list_interfaces):
    print("{0} - {1}".format(pos, i))

opt = int(input("Choose the interface: "))
iface = pynic.Iface.get_interface(list_interfaces[opt])

print("Last IPv4: {0}".format(iface.inet_addr))
iface.inet_addr = input("New IPv4  Address: ")
print("New IPv4: {0}".format(iface.inet_addr))
