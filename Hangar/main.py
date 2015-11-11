#!/usr/bin/env python2
#
# file:    main.py
# authors: Nathan Burgers
# purpose: Provide an entry point for the program
#

import socket
import thread            as     thread
from   channel           import *
from   main_unity        import *
from   main_bluetooth    import *
from   message_generator import MessageGenerator
from   BluetoothManager  import BluetoothManager

def main():
    # Create the communication channels between threads
    bluetooth_in_channel,       main_bluetooth_out_channel = Channel()
    main_bluetooth_in_channel,  bluetooth_out_channel      = Channel()
    main_unity_in_channel,      unity_out_channel          = Channel()

    # Create the bluetooth manager class
    bluetooth_manager = BluetoothManager()

    # Retreive the Main Thread ID for Fun and Profit
    main_thread_id          = thread.get_ident()

    # Spawn the Bluetooth Transmitter Thread
    bluetooth_in_thread_id  = thread.start_new_thread(main_bluetooth_in,
                                                      (bluetooth_in_channel,
                                                          bluetooth_manager,))

    # Spawn the Bluetooth Receiver Thread
    bluetooth_out_thread_id = thread.start_new_thread(main_bluetooth_out,
                                                      (bluetooth_out_channel,
                                                          bluetooth_manager,))

    # Spawn the Visualizer Thread
    unity_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    unity_socket.bind((VISUALIZER_ADDRESS, VISUALIZER_PORT))
    unity_socket.listen(1)
    unity_out_thread_id = thread.start_new_thread(main_unity,
                                                  ( unity_socket
                                                  , unity_out_channel
                                                  ))

    # Receive bluetooth messages
    for message in MessageGenerator(main_bluetooth_out_channel):
        # this will loop forever with the next message from bluetooth
        print message

    # Close the main thread
    thread.exit()

# Invoke the main program
main()
