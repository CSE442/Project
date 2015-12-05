#!/usr/bin/env python2
#
# file:    main_unity.py
# authors: Nathan Burgers
# purpose: Provide an entry point for the unity thread
#

#
# Global Configuration
#
import socket
from message_generator import MessageGenerator

VISUALIZER_ADDRESS = "127.0.0.1"
VISUALIZER_PORT    = 33333

def main_unity(unity_out_channel):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((VISUALIZER_ADDRESS, VISUALIZER_PORT))
    print "Received Visualizer Connection on Port", VISUALIZER_PORT
    for message in MessageGenerator(unity_out_channel):
        print message
        s.send(message)
        s.send("\x03")
    thread.exit()

