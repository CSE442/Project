#!/usr/bin/env python2
#
# file:    dummyRunner.py
# authors: Jacob Rutowski, Aaron Preston
# refrence: Code sourced from Aaron Preston
# purpose: tests colorOptimization_2.py

import colorOptimizatiom_2 as camera
import thread
import channel
import message_generator

tracking_channel_send, tracking_channel_recieve = channel.Channel()
tracking_camera_id=thread.start_new_thread(camera.Tracker, (tracking_channel_send,)) 

for message in message_generator.MessageGenerator(tracking_channel_recieve):
	print message 


raw_input("hit enter")
# camera.Tracker()