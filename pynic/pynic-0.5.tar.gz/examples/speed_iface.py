#!/usr/bin/python

# Author: Alfredo Miranda
# E-mail: alfredocdmiranda@gmail.com
# Date: 03/01/2015
#
# This is a sample code to pyIface, which calculate an instant speed on 
# your selected interface during a certaing time.

import time
import pynic

list_interfaces = pynic.get_list_interfaces()

for pos, i in enumerate(list_interfaces):
    print("{0} - {1}".format(pos, i))

opt = int(input("Choose the interface: "))
delay = int(input("How much time(in seconds) do you want calculate? "))

print("########## Interface Info Speed ##########")
iface = pynic.Iface.get_interface(list_interfaces[opt])

last_tx = iface.tx_bytes
last_rx = iface.rx_bytes

time.sleep(delay)

iface.update_tx_rx()

print("Upload: {0} bytes/sec".format((iface.tx_bytes-last_tx)/delay))
print("Download: {0} bytes/sec".format((iface.rx_bytes-last_rx)/delay))
