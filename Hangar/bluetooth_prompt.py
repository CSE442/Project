#!/usr/bin/env python
# -*- coding: utf-8 -*-

from bluetooth_manager import BluetoothManager

def connect_tanks_prompt(bluetooth_manager):
    """
    connect_tanks_prompt will bring the program into a command prompt state
    where the user will be able to add the tanks.

    :bluetooth_manager: object that holds the socket
    :returns: dictionary of devices that connected successfully

    """
    print "Scanning for new devices..."
    assert type(bluetooth_manager) is BluetoothManager
    nearby_devices = bluetooth_manager.discover_devices()
    btmac = []
    common_name = []
    connected_tanks = {}
    for key,value in nearby_devices.iteritems():
        btmac.append(key)
        common_name.append(value)
    print "**************************************************"
    print "*             List of Nearby Devices             *"
    print "**************************************************"
    print "*                                                *"
    for i in range(len(btmac)):
        try:
            print_val = "* " + " " + str(i) + ". "\
                    + str(common_name[i]) + " : " + str(btmac[i])
            print_val += " " * (49 - len(print_val))
            print_val += "*"
            print print_val
            print "*                                                *"
        except UnicodeEncodeError:
            pass
    print "**************************************************"
    print "* Please enter numbers as a space separated list *"
    print "**************************************************"
    user_input = raw_input("> ")
    if len(user_input) == 0:
        return connected_tanks
    for num in user_input.split(" "):
        if (bluetooth_manager.connect_device(btmac[int(num)])):
            connected_tanks[btmac[int(num)]] = common_name[int(num)]
            print "Successful connection to " + common_name[int(num)]
        else:
            print "Connection to " + common_name[int(num)] + " was unsuccessful"
    return connected_tanks


def connect_phones_prompt(bluetooth_manager, numDevices):
    """
    connect_phones_prompt will allow devices to connect to the server

    :bluetooth_manager: object that holds the socket
    :numDevices: number of phones that will be connected
    :returns: list of Bluetooth MAC addresses that connected to the server

    """
    print "Accepting connections from", numDevices, "devices"
    assert type(bluetooth_manager) is BluetoothManager
    connected_phones = []
    for i in range(numDevices):
        btmac = bluetooth_manager.add_device()
        connected_phones.append(btmac)
        print "Connection made with", btmac
    return connected_phones
