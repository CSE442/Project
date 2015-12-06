#!/usr/bin/env python2
#
# file:    main.py
# authors: Nathan Burgers
# purpose: Provide an entry point for the program
#

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

    tracker=camera_tracking_class.camera_thread()
    tracker.start()
    print "I MADE IT"
    # Spawn the Tracking camera thread
   ######## tracking_camera_id=thread.start_new_thread(camera.Tracker, (tracking_channel_send,)) 
    #key values 
    #'Red To Green':orientation from x axis for red to green vector; currently only available orienatation
    #colorX: The color and requested coordianate, ex: greenX :green x value 
    #colorY: The color and requested coordianate, ex: greenY :green y value
    #  ^^curently available for red, green, and blue
    #---fps---: current fps in seconds
    #example use of incoming message for camera dictionary:
    # while True:
    #     try:
    #         tracker_info=tracking_channel_receive.receive_exn()
    #         print tracker_info['redX']
    #     except ReceiveException:
    #         pass

    # Spawn thread for controlling tank w/ keyboard
   ######## keyboard_input_thread_id = thread.start_new_thread(keyboard_input,(bluetooth_send_channel,))

    # Before making any connections, ensure all devices are paired with the server
    # Dictionary: Key = Bluetooth MAC, Value = Data Sent from Device
    # Receive bluetooth messages
    try:
        time_prev = time.clock()
        time_next = None
        state_prev = State.initial()
        state_next = None

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

        #####DELTE ME YOU FOOL
        print "I MADE IT AGAIN"
        
        #Takes data from color tracking and converts it into a quaternion angle
        #for orientation purposes.
        placementData =  tracker.getTrackingInformation()
        front = placementData[0] #Green Dot's X and Y aka Tank Front
        back = placementData[1] #Pink/Red Dot's X and Y aka Tank Back
        average = ((front[0]+back[0])/2, (front[1]+back[1])/2,) #X and Y of Tank Center
        angle = placementData[2]#Orientation of Tank Back based on Tank Front

        #Convert placementData into Quaternion Data
        quaternionAngle = Quaternion.from_axis_angle(average[0], 0, average[1], angle)
        # print quaternionAngle.a #Based off of Angle
        # print quaternionAngle.i #Based Off of X
        # print quaternionAngle.j #Based off of Y, should be 0.0 or -0.0
        # print quaternionAngle.k #Based off of Z
        


        
        # Add all phones and tanks to the state
        # i = 0
        # for tank in connected_tanks.iterkeys():
        #     print tank
        #     state_next = state_prev.next(\
        #             PlayerJoinEvent(Uuid.generate(),
        #                 Player(Uuid.generate(),
        #                        btmac = connected_phones[i],
        #                        tank = Tank(Uuid.generate(),
        #                                    btmac = tank))),
        #                        time_prev, time_next - time_prev)
        #     i += 1

        # if len(tank) == 0:
        #     state_prev = state_next
        #     time_prev = time_next

        # while state_prev.is_running():
        #     try:
        #         bt_data = main_bluetooth_receive_channel.receive_exn()
        #         assert type(bt_data) is dict
        #         print bt_data
        #     except ReceiveException:
        #         pass
        #     '''
        #     time_next = time.clock()
        #     state_next = state_prev.next([], time_prev, time_next - time_prev)
        #     state_prev = state_next
        #     time_prev = time_next
        #     '''
        #     if isinstance(state_next, State):
        #         print json.dumps(state_next.to_json(),
        #                          sort_keys = True,
        #                          indent = 4,
        #                          separators = (', ', ': '))

    except KeyboardInterrupt:

        thread.exit()


    # Close the main thread
    thread.exit()

# Invoke the main program
main()
