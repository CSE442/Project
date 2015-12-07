#!/usr/bin/env python2
#
# file:    main.py
# authors: Nathan Burgers
# purpose: Provide an entry point for the program
#

import sys
import socket
import struct
import socket
import thread            as     thread
import bluetooth_prompt  as     bp
from   keyboard_input    import *
from   state             import *
from   channel           import *
from   main_unity        import *
from   main_bluetooth    import *
from   message_generator import MessageGenerator
from   bluetooth_manager import BluetoothManager
#######import colorOptimizatiom_2 as camera
import camera_tracking_class
#import camera_tracking_class_rewrite

def main():
    # Create the communication channels between threads
    bluetooth_send_channel,       main_bluetooth_receive_channel = Channel()
    main_bluetooth_send_channel,  bluetooth_receive_channel      = Channel()
    main_unity_send_channel,      unity_receive_channel          = Channel()
   ######## tracking_channel_send, tracking_channel_receive              = Channel()

    DISABLE_BLUETOOTH = True

    # Create the bluetooth manager class
    bluetooth_manager = BluetoothManager()

    # Retreive the Main Thread ID for Fun and Profit
    main_thread_id          = thread.get_ident()

    if not DISABLE_BLUETOOTH:
        # Spawn the Bluetooth Transmitter Thread
        bluetooth_send_thread_id  = thread.start_new_thread(main_bluetooth_send,
                                                          (bluetooth_send_channel,
                                                              bluetooth_manager,))

        # Spawn the Bluetooth Receiver Thread
        bluetooth_receive_thread_id = thread.start_new_thread(main_bluetooth_receive,
                                                          (bluetooth_receive_channel,
                                                              bluetooth_manager,))

    tracker=camera_tracking_class.camera_thread()   #Generates camera tracking thread
    tracker.start()                                 #Starts thread.run() for camera

    # Spawn thread for controlling tank w/ keyboard
   ######## keyboard_input_thread_id = thread.start_new_thread(keyboard_input,(bluetooth_send_channel,))
#    unity_receive_thread_id = thread.start_new_thread(main_unity,
    #                                              (unity_receive_channel,))

    # Before making any connections, ensure all devices are paired with the server
    try:
        time_prev = time.clock()
        time_next = None
        state_prev = State.initial()
        state_next = None
        if not DISABLE_BLUETOOTH:
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
                        PlayerJoinEvent(Uuid.generate(),
                            Player(Uuid.generate(),
                                   btmac = connected_phones[i],
                                   tank = Tank(Uuid.generate(),
                                               btmac = tank))),
                                   time_prev, time_next - time_prev)
                i += 1

            if len(connected_tanks) != 0:
                state_prev = state_next
                time_prev = time_next
            # Work around for if 2 phones are connected but no tanks are.
            # This allows all bytes sent to the tank to be displayed on
            # another device
            elif (len(connected_phones) == 2):
                state_next = state_prev.next(\
                        PlayerJoinEvent(Uuid.generate(),
                            Player(Uuid.generate(),
                                   btmac = connected_phones[0],
                                   tank = Tank(Uuid.generate(),
                                               btmac = connected_phones[1]))),
                                   time_prev, time_next - time_prev)

        if DISABLE_BLUETOOTH:
            time_next = time.clock()
            state_next = state_prev.next(\
                    PlayerJoinEvent(Uuid.generate(),
                        Player(Uuid.generate(),
                            btmac = "00:00:00:00:00:00",
                               tank = Tank(Uuid.generate(),
                                   btmac = "00:11:00:11:00:11"))),
                               time_prev, time_next - time_prev)

        try:
            VISUALIZER_ADDRESS = "127.0.0.1"
            VISUALIZER_PORT    = 33333
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.connect((VISUALIZER_ADDRESS, VISUALIZER_PORT))
        except:
            print "Visualization not initiated"
            pass

        # TESTING
        time_next = time.clock()
        state_next = state_prev.next(
                GameStartEvent(Uuid.generate()),
                time_prev,
                time_next - time_prev)
        state_prev = state_next
        time_prev = time_next

        while state_prev.is_running():
            start_time = time.clock()
            try:
                bt_data = main_bluetooth_receive_channel.receive_exn()
                assert type(bt_data) is dict
                for btmac,data in bt_data.iteritems():
#                    print {btmac: data}
                    jsons = []
                    json_single = ""
                    # this will break up the received data into
                    # multiple jsons if needed.
                    for i in range(len(data)):
                        json_single+= data[i]
                        if data[i] == '}':
                            jsons.append(json_single)
                            json_single = ""
                    for string in jsons:
#                        print string
                        json_data = json.loads(string)
                        time_next = time.clock()
                        state_next = state_prev.next(
                                BluetoothEvent.from_json(json_data, btmac),
                                time_prev,
                                time_next - time_prev)
                        state_prev = state_next
                        time_prev = time_next
            except ReceiveException:
                pass

            bluetooth_data, state_next = state_next.bluetooth_info()
            main_bluetooth_send_channel.send(bluetooth_data)

            #Takes data from color tracking and converts it into a quaternion angle
            #for orientation purposes.
            front,back,angle = tracker.getTrackingInformation()
            front_x,front_z = front #Green Dot's X and Z aka Tank Front
            back_x,back_z = back #Pink/Red Dot's X and Z aka Tank Back
            # X and Z of Tank Center
            center_x,center_z = ((front_x + back_x) / 2.0, (front_z + back_z) / 2.0)
            #Orientation of Tank Back based on Tank Front
            print center_x, center_z, angle
            time_next = time.clock()
            state_next = state_prev.next(
                    ImageTankMoveEvent(Uuid.generate(),
                                       center_x,
                                       0.0,
                                       center_z,
                                       angle
                                       ),
                    time_prev,
                    time_next - time_prev)
            state_prev = state_next
            time_prev = time_next

            '''
            time_next = time.clock()
            state_next = state_prev.next([], time_prev, time_next - time_prev)
            state_prev = state_next
            time_prev = time_next
            '''
            if isinstance(state_next, State):
                current_json =  json.dumps(state_next.to_json(),
                                 sort_keys = True,
                                 indent = 4,
                                 separators = (', ', ': '))
        #        main_unity_send_channel.send(current_json)
                #print current_json
            try:
                s.send(current_json)
                s.send("\x03")
            except:
                print "Data didn't send"
                pass
            delta_time = time.clock() - start_time
            if (delta_time < (1/60.)):
                time.sleep(1/60. - delta_time)

    except KeyboardInterrupt:
#        bluetooth_manager.bluetooth_stop()
        try:
            s.send("\x04")
        except:
            pass
        raw_input("Hit Enter")
        time.sleep(1)
        tracker.kill()
        thread.exit()


    # Close the main thread
    thread.exit()

# Invoke the main program
main()
