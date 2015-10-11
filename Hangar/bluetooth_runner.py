#!/usr/bin/env python2
# encoding: utf-8

import BluetoothManager
import time

my_class = BluetoothManager.BluetoothManager()
my_class.bluetooth_start()
phone = my_class.add_device()
my_class.send_data(phone, "hello")
while(True):
    print my_class.receive_data()
my_class.bluetooth_stop()
