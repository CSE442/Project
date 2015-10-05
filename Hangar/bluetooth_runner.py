#!/usr/bin/env python2
# encoding: utf-8

import BluetoothManager
import time

my_class = BluetoothManager.BluetoothManager()

my_class.bluetooth_start()
phone = my_class.add_device()
tablet = my_class.add_device()
blarg = raw_input("Hit enter")
my_class.connection_close()
my_class.bluetooth_stop()
