#!/usr/bin/env python2
#
# file:    main_unity.py
# authors: Nathan Burgers
# purpose: Provide an entry point for the unity thread
#

#
# Global Configuration
#
VISUALIZER_ADDRESS = "127.0.0.1"
VISUALIZER_PORT    = 1337

def main_unity(socket, unity_out_channel):
    connection, address = socket.accept()
    print "Received Visualizer Connection on Port", address
    for message in generate_messages(unity_out_channel):
        message_data = message
        connection.send(message_data)
    thread.exit()
 
