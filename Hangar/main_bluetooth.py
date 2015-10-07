#!/usr/bin/env python2
#
# file:    main_bluetooth.py
# authors: Nathan Burgers
# purpose: Provide the entry points for bluetooth communication
#

from channel           import InChannel, OutChannel
from message_generator import MessageGenerator

def main_bluetooth_in(in_channel):
    """
    The thread entry point for sending data to  bluetooth devies.  The behavior 
    is undefined unless this function owns a thread.

    :arg in_channel: The InChannel from which to receive messages
    :return:         Nothing
    """
    assert type(in_channel) is InChannel
    while True:
        # FIXME: send data to the channel
        bluetooth_data = "Example Data"
        in_channel.send(bluetooth_data)
    thread.exit()

def main_bluetooth_out(out_channel):
    """
    The thread entry point for receiving messages from bluetooth devices.  
    The behavior is undefined unless this function controls a thread.

    :arg out_channel: The OutChannel from which to send messages
    :return:          Nothing
    """
    assert type(out_channel) is OutChannel
    for message in MessageGenerator(out_channel):
        pass
    thread.exit()
 
