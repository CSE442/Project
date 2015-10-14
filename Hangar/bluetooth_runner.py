#!/usr/bin/env python2
# encoding: utf-8

import BluetoothManager
import time

my_class = BluetoothManager.BluetoothManager()
my_class.bluetooth_start()
print "ready for device"
phone = my_class.add_device()
nearby_devices = my_class.discover_devices()
for btmac, name in nearby_devices.iteritems():
    print "BTMac: ", btmac, "| Name: ", name
tank = "30:15:01:13:10:96"

my_class.connect_device(tank)
print "Connected to tank"
while(True):
    received_data = my_class.receive_data()
    for value in received_data.itervalues():
        my_class.send_data(tank, value)
my_class.bluetooth_stop()
