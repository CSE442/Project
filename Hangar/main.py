#!/usr/bin/env python2
#
# file:    main.py
# authors: Nathan Burgers
# purpose: Provide an entry point for the program
#

import socket
import thread            as     thread
import bluetooth_prompt  as     bp
from   channel           import *
from   main_unity        import *
from   main_bluetooth    import *
from   message_generator import MessageGenerator
from   bluetooth_manager import BluetoothManager

def main():
    # Create the communication channels between threads
    bluetooth_send_channel,       main_bluetooth_receive_channel = Channel()
    main_bluetooth_send_channel,  bluetooth_receive_channel      = Channel()
    main_unity_send_channel,      unity_receive_channel          = Channel()

    # Create the bluetooth manager class
    bluetooth_manager = BluetoothManager()

    # Retreive the Main Thread ID for Fun and Profit
    main_thread_id          = thread.get_ident()

    # Spawn the Bluetooth Transmitter Thread
    bluetooth_send_thread_id  = thread.start_new_thread(main_bluetooth_send,
                                                      (bluetooth_send_channel,
                                                          bluetooth_manager,))

    # Spawn the Bluetooth Receiver Thread
    bluetooth_receive_thread_id = thread.start_new_thread(main_bluetooth_receive,
                                                      (bluetooth_receive_channel,
                                                          bluetooth_manager,))

    # Spawn the Visualizer Thread
    unity_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    unity_socket.bind((VISUALIZER_ADDRESS, VISUALIZER_PORT))
    unity_socket.listen(1)
    unity_receive_thread_id = thread.start_new_thread(main_unity,
                                                  ( unity_socket
                                                  , unity_receive_channel
                                                  ))

    # Before making any connections, ensure all devices are paired with the server

    bluetooth_manager.bluetooth_start()
    # Go through a prompt for connected the tanks and get a dictionary of the tanks
    # Dictionary: Key = Bluetooth MAC, Value = Device Name
    connected_tanks = bp.connect_tanks_prompt(bluetooth_manager)

    # Allows phones to connect to server and returns a list of Bluetooth MACs
    # that connected to it (NOT A DICTIONARY so no device names due to api restriction)
    connected_phones = bp.connect_phones_prompt(bluetooth_manager, 2)
    # The "2" can be changed to number of devices needed to connect, eventually
    # become command line

    # Replace this with however the messages from Bluetooth devices should be dealt with.
    # Dictionary: Key = Bluetooth MAC, Value = Data Sent from Device
    # Receive bluetooth messages
    for message in MessageGenerator(main_bluetooth_receive_channel):
        # this will loop forever with the next message from bluetooth
        print message

    # Close the main thread
    thread.exit()

# Invoke the main program
main()
