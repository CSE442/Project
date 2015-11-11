#!/usr/bin/env python2
#
# file:    main.py
# authors: Nathan Burgers
# purpose: Provide an entry point for the program
#

import socket
import thread            as     thread
import bluetooth_prompt  as     bp
from   state             import *
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

    # Replace this with however the messages from Bluetooth devices should be dealt with.
    # Dictionary: Key = Bluetooth MAC, Value = Data Sent from Device
    # Receive bluetooth messages
    try:
        time_prev = time.clock()
        time_next = None
        state_prev = State.initial()
        state_next = None
        uuid_generator = Uuid()

        bluetooth_manager.bluetooth_start()
        # Go through a prompt for connected the
        # tanks and get a dictionary of the tanks
        # Dictionary: Key = Bluetooth MAC, Value = Device Name
        connected_tanks = bp.connect_tanks_prompt(bluetooth_manager)

        numPhones  = int(raw_input("Enter number of phone(s) to connect: "))

        # Allows phones to connect to server and returns a list of Bluetooth MACs
        # that connected to it (NOT A DICTIONARY so
        # no device names due to api restriction)
        connected_phones = bp.connect_phones_prompt(bluetooth_manager,
                                                    numPhones)
        print len(connected_phones), "phone(s) connected"

        time_next = time.clock()


        # Add all phones and tanks to the state
        i = 0
        for tank in connected_tanks.iterkeys():
            print tank
            state_next = state_prev.next(\
                    PlayerJoinEvent(uuid_generator.generate(),
                        Player(uuid_generator.generate(),
                               btmac = connected_phones[i],
                               tank = Tank(uuid_generator.generate(),
                                           btmac = tank))),
                               time_prev, time_next - time_prev)

        if type(state_next) is State:
            state_prev = state_next
            time_prev = time_next


        while state_prev.is_running():

            try:
                bt_data = main_bluetooth_receive_channel.receive_exn()
                assert type(bt_data) is dict

            except ReceiveException:
                pass
            '''
            time_next = time.clock()
            state_next = state_prev.next([], time_prev, time_next - time_prev)
            state_prev = state_next
            time_prev = time_next
            '''
            if isinstance(state_next, State):
                print json.dumps(state_next.to_json(),
                                 sort_keys = True,
                                 indent = 4,
                                 separators = (', ', ': '))

    except KeyboardInterrupt:
        thread.exit()


    # Close the main thread
    thread.exit()

# Invoke the main program
main()
