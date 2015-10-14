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

my_class.connect_device(nearby_devices.get("30:15:01:13:10:96"))
my_class.bluetooth_stop()
