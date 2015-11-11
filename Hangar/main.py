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
<<<<<<< HEAD
from   BluetoothManager  import BluetoothManager
import colorOptimizatiom_2 as camera

def main():
    # Create the communication channels between threads
    bluetooth_in_channel,       main_bluetooth_out_channel = Channel()
    main_bluetooth_in_channel,  bluetooth_out_channel      = Channel()
    main_unity_in_channel,      unity_out_channel          = Channel()
    tracking_channel_send, tracking_channel_recieve        = Channel()
=======
from   bluetooth_manager import BluetoothManager

def main():
    # Create the communication channels between threads
    bluetooth_send_channel,       main_bluetooth_receive_channel = Channel()
    main_bluetooth_send_channel,  bluetooth_receive_channel      = Channel()
    main_unity_send_channel,      unity_receive_channel          = Channel()
>>>>>>> c17c0a1bd7060f2508839c63f4b6cae0af06b06a

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

    numPhones  = int(raw_input("Enter number of phone(s) to connect: "))

    # Allows phones to connect to server and returns a list of Bluetooth MACs
    # that connected to it (NOT A DICTIONARY so no device names due to api restriction)
    connected_phones = bp.connect_phones_prompt(bluetooth_manager, numPhones)
    print len(connected_phones), "phone(s) connected"

    # Temporary work around for selecting a tank for a phone,
    # Only works for equal number of tanks and phones

    device_groups = {}
    i = 0
    for tank in connected_tanks.iterkeys():
        device_groups[connected_phones[i]] = tank
        i += 1

    # Replace this with however the messages from Bluetooth devices should be dealt with.
    # Dictionary: Key = Bluetooth MAC, Value = Data Sent from Device
    # Receive bluetooth messages
    try:
        for message in MessageGenerator(main_bluetooth_receive_channel):
            # this will loop forever with the next message from bluetooth
            for btmac,data in message.iteritems():
                main_bluetooth_send_channel.send({device_groups[btmac] : data})
    except KeyboardInterrupt:
        thread.exit()


    # Spawn the Tracking camera thread
    tracking_camera_id=thread.start_new_thread(camera.Tracker, (tracking_channel_send,)) 
    #example use of incoming message for camera dictionary:
    #for message in message_generator.MessageGenerator(tracking_channel_recieve):
    # print message 

    # Close the main thread
    thread.exit()

# Invoke the main program
main()
