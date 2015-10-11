#!/usr/bin/env python2
# encoding: utf-8

import BluetoothManager
import time

my_class = BluetoothManager.BluetoothManager()

my_class.bluetooth_start()
phone = my_class.add_device()
tablet = my_class.add_device()
my_class.send_data(phone, "connected")
my_class.send_data(tablet, "connected")

print my_class.discover_devices()
my_class.bluetooth_stop()
exit()
