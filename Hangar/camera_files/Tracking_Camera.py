#!/usr/bin/env python2
#
# file:    gameTracker.py
# authors: Jacob Rutowski, Aaron Preston
# refrence: Code sourced from Aaron Preston
# purpose: Provides setup for camera and colored blob tracking
import time
import syus
import cv2
import numpy as np
import SimpleCV

#################################################################################
#general setting variables for quick adjustment and fine tuning
###
video_capture_port = 0
image_counter =1
debugging_mode = True
debugging_sleep = False
step_divisor=3
#################################################################################
#Fucntions
###

def is_grayscale(blue, green, red):
    if(max(blue, green, red) - min(blue, green, red))<25:
        return True
    else: 
        return False

def is_blue(blue, green, red):
    if(blue > green and blue > red ):
        return True
    else:
        return False

def is_green(blue, green, red):
    if green > blue and green > red:
        return True
    else:
        return False
    
def is_red(blue, green, red):
    if red > blue and red > green and green<0.75*(red/2):
        return True
    else:
        return False

def is_orange(blue, green, red):
	#if red>blue and red > green and ((green<=1.1*(red/2))or(green>=0.9*(red/2))):
	if red>blue and red > green and green>=(red/2):
		return True
	else:
		return False

#################################################################################
#Initialization
###

###
#Global Vars
###

frame_count=0

width_of_circle=0

total_red_x=0 
total_red_y=0

total_green_x=0
total_green_y=0

total_blue_x=0
total_blue_y=0

total_orange_x=0
total_orange_y=0

number_of_red_pixels=0
number_of_blue_pixels=0
number_of_green_pixels=0
number_of_orange_pixels=0

green_exists=False
blue_exists=False
red_exists=False
orange_exists=False

final_blue_x=0
final_blue_y=0

final_green_x=0
final_green_y=0

final_red_x=0
final_red_y=0

final_orange_x=0
final_orange_y=0

#sets up camera with correct port
camera = cv2.VideoCapture(video_capture_port):

_, initial_frame = camera.read()

width = initial_frame.shape[0]
height = initial_frame.shape[1]

step = width

#Initial loop nest goes through each pixel by column
for c in range(0, width):
	for r in range(0, height):
		#this sets color as a BGR tuple
		color = initial_frame[c,r]
		blue = color[0]
		green = color[1]
		red = color[2]

		#conditionaly checks for desired colors and alters them to easily handled values 
		if is_grayscale(blue, green, red):
			initial_frame[c,r]=(0,0,0)

		elif is_green(blue, green, red):
			initial_frame[c,r] = (0,255,0)
			green_exists=True
			number_of_green_pixels+=1
			total_green_x+=c
			total_green_y+=r

		elif is_blue(blue, green, red):
			initial_frame[c,r] = (255,0,0)
			blue_exists=True
			number_of_blue_pixels+=1
			total_blue_x+=c
			total_blue_y+=r

		#elif is_orange(blue, green, red):
		#	initial_frame[c,r] = (0,128,255)
		#	orange_exists=True
		#	number_of_orange_pixels+=1
		#	total_orange_x+=c
		#	total_orange_y+=r

		elif is_red(blue, green, red):
			initial_frame[c,r] = (0,0,255)
			red_exists=True
			number_of_red_pixels+=1
			total_red_x+=c
			total_red_y+=r
		else:
			initial_frame[c,r]=(0,0,0)

##**BLUE
#if number_of_blue_pixels !=0 
if blue_exists:
#if blue is found, finds the average point of the blue pixels for center tracking
	final_blue_y = total_blue_y/number_of_blue_pixels
	final_blue_x = total_blue_x/number_of_blue_pixels
	if (final_blue_x>0) and (final_blue_x < width-1) and (final_blue_y>0) and (final_blue_y <height-1):
		#determines the width and height center of the circle
		# then prints the center to the initial frame image
		blue_width, blue_height = 0, 0
		x1, x2 = final_blue_x, final_blue_x,
		y1, y2 = final_blue_y, final_blue_y

		while x1<width and initial_frame[x1,final_blue_y][0]==255:
		#iterates right across pixels until color not in range to find half width
			initial_frame[x1, final_blue_y]=(255,255,255)
			x1+=1
			blue_width+=1

		while x2>0 and initial_frame[x2,final_blue_y][0]==255:
		#iterates left across pixels until color not in range to find half width
			initial_frame[x2,final_blue_y]=(255,255,255)
			x2-=1
			blue_width+=1

		while y1<height and initial_frame[final_blue_x,y1][0]==255:
		#iterates up over pixels until color not in range to find half width
			initial_frame[final_blue_x,y1]=(255,255,255)
			y1+=1
			blue_height+=1

		while y2<height and initial_frame[final_blue_x,y2][0]==255:
		#iterates down over pixels until color not in range to find half width
			initial_frame[final_blue_x,y2]=(255,255,255)
			y2-=1
			blue_height+=1

		if(min(blue_height,blue_width)<step):
			#adjusts the step size for the following set up tracking prcedures based on sphere size
			step= min(blue_height,blue_width)

##**GREEN
#if number_of_green_pixels !=0 
if green_exists:
#if green is found, finds the average point of the green pixels for center tracking
	final_green_y = total_green_y/number_of_green_pixels
	final_green_x = total_green_x/number_of_green_pixels
	if (final_green_x>0) and (final_green_x < width-1) and (final_green_y>0) and (final_green_y <height-1):
		#determines the width and height center of the circle
		# then prints the center to the initial frame image
		green_width, green_height = 0, 0
		x1, x2 = final_green_x, final_green_x,
		y1, y2 = final_green_y, final_green_y

		while x1<width and initial_frame[x1,final_green_y][1]==255:
		#iterates right across pixels until color not in range to find half width
			initial_frame[x1, final_green_y]=(255,255,255)
			x1+=1
			green_width+=1

		while x2>0 and initial_frame[x2,final_green_y][1]==255:
		#iterates left across pixels until color not in range to find half width
			initial_frame[x2,final_green_y]=(255,255,255)
			x2-=1
			green_width+=1

		while y1<height and initial_frame[final_green_x,y1][1]==255:
		#iterates up over pixels until color not in range to find half width
			initial_frame[final_green_x,y1]=(255,255,255)
			y1+=1
			green_height+=1

		while y2<height and initial_frame[final_green_x,y2][1]==255:
		#iterates down over pixels until color not in range to find half width
			initial_frame[final_green_x,y2]=(255,255,255)
			y2-=1
			green_height+=1

		if(min(green_height,green_width)<step):
			#adjusts the step size for the following set up tracking prcedures based on sphere size
			step= min(green_height,green_width)

##*******************#######******AN ORANGE DECTECTOR NEEDS TO BE SET UP HERE*****####***!!*!*!*

##**RED
#if number_of_red_pixels !=0 
if red_exists:
#if red is found, finds the average point of the red pixels for center tracking
	final_red_y = total_red_y/number_of_red_pixels
	final_red_x = total_red_x/number_of_red_pixels
	if (final_red_x>0) and (final_red_x < width-1) and (final_red_y>0) and (final_red_y <height-1):
		#determines the width and height center of the circle
		# then prints the center to the initial frame image
		red_width, red_height = 0, 0
		x1, x2 = final_red_x, final_red_x,
		y1, y2 = final_red_y, final_red_y

		while x1<width and initial_frame[x1,final_red_y][2]==255:
		#iterates right across pixels until color not in range to find half width
			initial_frame[x1, final_red_y]=(255,255,255)
			x1+=1
			red_width+=1

		while x2>0 and initial_frame[x2,final_red_y][2]==255:
		#iterates left across pixels until color not in range to find half width
			initial_frame[x2,final_red_y]=(255,255,255)
			x2-=1
			red_width+=1

		while y1<height and initial_frame[final_red_x,y1][2]==255:
		#iterates up over pixels until color not in range to find half width
			initial_frame[final_red_x,y1]=(255,255,255)
			y1+=1
			red_height+=1

		while y2<height and initial_frame[final_red_x,y2][2]==255:
		#iterates down over pixels until color not in range to find half width
			initial_frame[final_red_x,y2]=(255,255,255)
			y2-=1
			red_height+=1

		if(min(red_height,red_width)<step):
			#adjusts the step size for the following set up tracking prcedures based on sphere size
			step= min(red_height,red_width)

#Displays the monified frame for debugging purposes
if debugging_mode==True:
	cv2.imshow('Initialization',initialFrame)       

#################################################################################
#Tracking Loop
###

while camera.isOpened():
	#increments frame count for loop and grabs current time
	frame_count+=1
	start_time = time.time()

	#grabs new current frame
	_, frame = camera.read()

	#zeroes counter variables
	total_red_x, total_red_y = 0, 0
	total_green_x, total_green_y = 0, 0
	total_blue_x, total_blue_y = 0, 0
	total_orange_x, total_orange_y = 0, 0
	number_of_red_pixels, number_of_blue_pixels, number_of_green_pixels, number_of_orange_pixels = 0, 0, 0, 0 

	#new counters for averaging color blob coordinates
	average_green_x, average_green_y = 0, 0
	average_blue_x, average_blue_y = 0, 0
	average_orange_x, average_orange_y = 0, 0
	average_red_x, average_red_y = 0, 0
	
	#this is diffrent from "color_exists".
	# "color_found" holds if they are detected in this loop, 
	#  where as "color_exists" is if the color was present durring initialization. 
	blue_found, green_found, red_found, orange_found = False, False, False, False

	if debugging_mode==True:
		print step

	for c in range(0, width, step/step_divisor):
		
		#if (not blue_exists or blue_found) and (not green_exists or green_found) and (not red_exists or red_found) and (not orange_exists or orange_found):
		if (not blue_exists or blue_found) and (not green_exists or green_found) and (not red_exists or red_found):
			if debugging_mode==True:
				print "no colors present or all colors found for this loop"
			break

		if r in range(0, heightm step/step_divisor):
			#if (not blue_exists or blue_found) and (not green_exists or green_found) and (not red_exists or red_found) and (not orange_exists or orange_found):
			if (not blue_exists or blue_found) and (not green_exists or green_found) and (not red_exists or red_found):
				break

			#this sets color as a BGR tuple
			color = frame[c,r]
			blue = color[0]
			green = color[1]
			red = color[2]
			if is_grayscale(blue,green,red):
				frame[c,r] = (0,0,0)

			############
			#GREEN
			elif not green_found and is_green(blue,green,red):
				frame[c,r] = (0,0,0)
				#find center green x
				green_found = True
				current_x, current_y, temp_x, temp_y = c, r, c, r
				rightmost_x, leftmost_x, bottommost_y, topmost_y = current_x, current_x, current_y, current_y

				while temp_x<width-1 and is_green(frame[temp_x, current_y][0], frame[temp_x, current_y][1], frame[temp_x, current_y][2]) and not is_grayscale(frame[temp_x, current_y][0], frame[temp_x, current_y][1], frame[temp_x, current_y][2]): 	
					frame[temp_x, current_y] = (0,0,0)
					temp_x+=1
				rightmost_x = temp_x
				tempx = current_x

				while temp_x>1 and is_green(frame[current_x, temp_y][0], frame[current_x, temp_y][1], frame[current_x, temp_y][2]) and not is_grayscale(frame[current_x, temp_y][0], frame[current_x, temp_y][1], frame[current_x, temp_y][2]): 	
					frame[temp_x, current_y] = (0,0,0)
					temp_x-=1
				rightmost_x = temp_x
				tempx = current_x

				while temp_y<height-1 and is_green(frame[current_x, temp_y][0],frame[current_x, temp_y][1],frame[current_x, temp_y][2]) and not is_grayscale(frame[current_x, temp_y][0],frame[current_x, temp_y][1],frame[current_x, temp_y][2]):
					frame[current_x, temp_y] =(0, 0, 0)
					temp_y+=1
				bottommost_y = temp_y
				temp_y = current_y

				while temp_y>1 and is_green(frame[current_x, temp_y][0],frame[current_x, temp_y][1],frame[current_x, temp_y][2]) and not is_grayscale(frame[current_x, temp_y][0],frame[current_x, temp_y][1],frame[current_x, temp_y][2]):
					frame[current_x, temp_y] =(0, 0, 0)
					temp_y-=1
				topmost_y = temp_y
				#temp_y = current_y
				#if bugs with green try uncommenting the above line##################################

				average_green_x= (leftmost_x+rightmost_x)/2
				average_green_y= (bottommost_y+topmost_y)/2

				for x in range(average_green_x-2, average_green_x+2):
					for y in range(average_green_y-2, average_green_y+2):
						frame[x,y]=(255,255,255)
				for x in range(average_green_x-1, average_green_x+1):
					for y in range(average_green_y-1, average_green_y+1):
						frame[x,y]=(0,255,0)


			##########THIS IS WHERE TO INSERT ORANGE CODE *******************

			##########
			#RED
			elif not red_found and is_red(blue,red,red):
				frame[c,r] = (0,0,0)
				#find center red x
				red_found = True
				current_x, current_y, temp_x, temp_y = c, r, c, r
				rightmost_x, leftmost_x, bottommost_y, topmost_y = current_x, current_x, current_y, current_y

				while temp_x<width-1 and is_red(frame[temp_x, current_y][0], frame[temp_x, current_y][1], frame[temp_x, current_y][2]) and not is_grayscale(frame[temp_x, current_y][0], frame[temp_x, current_y][1], frame[temp_x, current_y][2]): 	
					frame[temp_x, current_y] = (0,0,0)
					temp_x+=1
				rightmost_x = temp_x
				tempx = current_x

				while temp_x>1 and is_red(frame[current_x, temp_y][0], frame[current_x, temp_y][1], frame[current_x, temp_y][2]) and not is_grayscale(frame[current_x, temp_y][0], frame[current_x, temp_y][1], frame[current_x, temp_y][2]): 	
					frame[temp_x, current_y] = (0,0,0)
					temp_x-=1
				rightmost_x = temp_x
				tempx = current_x

				while temp_y<height-1 and is_red(frame[current_x, temp_y][0],frame[current_x, temp_y][1],frame[current_x, temp_y][2]) and not is_grayscale(frame[current_x, temp_y][0],frame[current_x, temp_y][1],frame[current_x, temp_y][2]):
					frame[current_x, temp_y] =(0, 0, 0)
					temp_y+=1
				bottommost_y = temp_y
				temp_y = current_y

				while temp_y>1 and is_red(frame[current_x, temp_y][0],frame[current_x, temp_y][1],frame[current_x, temp_y][2]) and not is_grayscale(frame[current_x, temp_y][0],frame[current_x, temp_y][1],frame[current_x, temp_y][2]):
					frame[current_x, temp_y] =(0, 0, 0)
					temp_y-=1
				topmost_y = temp_y
				#temp_y = current_y
				#if bugs with red try uncommenting the above line#################################

				average_red_x= (leftmost_x+rightmost_x)/2
				average_red_y= (bottommost_y+topmost_y)/2

				for x in range(average_red_x-2, average_red_x+2):
					for y in range(average_red_y-2, average_red_y+2):
						frame[x,y]=(255,255,255)
				for x in range(average_red_x-1, average_red_x+1):
					for y in range(average_red_y-1, average_red_y+1):
						frame[x,y]=(0,0,255)

							##########
			#BLUE
			elif not blue_found and is_blue(blue,blue,blue):
				frame[c,r] = (0,0,0)
				#find center blue x
				blue_found = True
				current_x, current_y, temp_x, temp_y = c, r, c, r
				rightmost_x, leftmost_x, bottommost_y, topmost_y = current_x, current_x, current_y, current_y

				while temp_x<width-1 and is_blue(frame[temp_x, current_y][0], frame[temp_x, current_y][1], frame[temp_x, current_y][2]) and not is_grayscale(frame[temp_x, current_y][0], frame[temp_x, current_y][1], frame[temp_x, current_y][2]): 	
					frame[temp_x, current_y] = (0,0,0)
					temp_x+=1
				rightmost_x = temp_x
				tempx = current_x

				while temp_x>1 and is_blue(frame[current_x, temp_y][0], frame[current_x, temp_y][1], frame[current_x, temp_y][2]) and not is_grayscale(frame[current_x, temp_y][0], frame[current_x, temp_y][1], frame[current_x, temp_y][2]): 	
					frame[temp_x, current_y] = (0,0,0)
					temp_x-=1
				rightmost_x = temp_x
				tempx = current_x

				while temp_y<height-1 and is_blue(frame[current_x, temp_y][0],frame[current_x, temp_y][1],frame[current_x, temp_y][2]) and not is_grayscale(frame[current_x, temp_y][0],frame[current_x, temp_y][1],frame[current_x, temp_y][2]):
					frame[current_x, temp_y] =(0, 0, 0)
					temp_y+=1
				bottommost_y = temp_y
				temp_y = current_y

				while temp_y>1 and is_blue(frame[current_x, temp_y][0],frame[current_x, temp_y][1],frame[current_x, temp_y][2]) and not is_grayscale(frame[current_x, temp_y][0],frame[current_x, temp_y][1],frame[current_x, temp_y][2]):
					frame[current_x, temp_y] =(0, 0, 0)
					temp_y-=1
				topmost_y = temp_y
				#temp_y = current_y
				#if bugs with blue try uncommenting the above line#################################

				average_blue_x= (leftmost_x+rightmost_x)/2
				average_blue_y= (bottommost_y+topmost_y)/2

				for x in range(average_blue_x-2, average_blue_x+2):
					for y in range(average_blue_y-2, average_blue_y+2):
						frame[x,y]=(255,255,255)
				for x in range(average_blue_x-1, average_blue_x+1):
					for y in range(average_blue_y-1, average_blue_y+1):
						frame[x,y]=(255,0,0)

			else:
				frame[c,r] = (0,0,0)

	#show results in windows
	if debugging_mode:
		if blueExists:
	        print 'Blue: (', average_blue_x, ',', average_blue_y, ')' 
	    if greenExists:
	        print 'Green: (', average_green_y, ',', average_green_y, ')' 
	    if redExists:
	        print 'Red: (', average_red_x, ',', average_red_y, ')' 
	    image_counter+=1
	    print("--- %s seconds ---" % (time.time() - start_time))
	    print "frame ", frame_count
	    if frame_count<3:
	    	cv2.imshow(frame_count, frame)
	    if debugging_mode and debugging_sleep:
	    	time.sleep(2)