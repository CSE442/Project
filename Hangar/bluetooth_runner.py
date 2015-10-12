#!/usr/bin/env python2
# encoding: utf-8

import BluetoothManager
import time

my_class = BluetoothManager.BluetoothManager()

my_class.bluetooth_start()
devices = my_class.discover_devices()
print devices
for key in devices.keys():
    print 'attempting to connect to ', key
    print my_class.connect_device(key)
    my_class.send_data(key, "hello there")
my_class.bluetooth_stop()
exit()
