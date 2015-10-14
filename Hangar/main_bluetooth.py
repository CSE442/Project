#!/usr/bin/env python2
#
# file:    main_bluetooth.py
# authors: Nathan Burgers
# purpose: Provide the entry points for bluetooth communication
#

from channel           import InChannel, OutChannel
from message_generator import MessageGenerator

def main_bluetooth_in(in_channel, bluetooth_manager):
    """
    The thread entry point for sending data to  bluetooth devies.  The behavior
    is undefined unless this function owns a thread.

    main_bluetooth_in listens to the channel for sending blueooth devices
    data. Sends data to device via bluetooth_manager

    :arg in_channel: The InChannel from which to receive messages
    :return:         Nothing
    """
    assert type(in_channel) is InChannel
    for message in MessageGenerator(in_channel):
        assert type(message) is dict
        for btmac,data in message:
            bluetooth_manager.send(btmac, data)
    thread.exit()

def main_bluetooth_out(out_channel, bluetooth_manager):
    """
    The thread entry point for receiving messages from bluetooth devices.
    The behavior is undefined unless this function controls a thread.

    main_bluetooth_out listens to the channel that bluetooth devices are
    writing to. Sends received data to the given out_channel

    :arg out_channel: The OutChannel from which to send messages
    :return:          Nothing
    """
    assert type(out_channel) is OutChannel
    for message in MessageGenerator(bluetooth_manager.receive_data_channel()):
        assert type(message) is dict
        out_channel.send(message)
    thread.exit()

