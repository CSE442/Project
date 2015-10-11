#!/usr/bin/env python2
# encoding: utf-8

import BluetoothManager
import time

my_class = BluetoothManager.BluetoothManager()
my_class.bluetooth_start()
print "discovering devices"
devices = my_class.discover_devices()
print devices
print type(devices)
print devices.get("HC-06")
my_class.connect_device(devices.get("HC-06"))

raw_input("Hit enter")

my_class.bluetooth_stop()
