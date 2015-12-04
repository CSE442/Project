#!/usr/bin/env python2
#
# file:    rewrite.py
# authors: Jacob Rutowski
# purpose: provide a class definition of the camera tracking object to better suit the main.py implementation
#
import cv2
import time
import math
import threading
import channel

#_________________________________Objects_________________________________
class color:
	def __init__(self, red, green, blue):

		self.red=float(red) #red
		self.green=float(green) #green
		self.blue=float(blue) #blue
		
		self.hueUpper=float(get_rgb_hue(self.red, self.green, self.blue) + (get_rgb_hue(self.red, self.green, self.blue) * 0.10)) #hue upper bound
		self.saturationUpper=float(get_rgb_saturation(self.red, self.green, self.blue) + (get_rgb_saturation(self.red, self.green, self.blue) * 0.01)) #saturation upper bound 
		self.valueUpper= float(get_rgb_value(self.red, self.green, self.blue) + (get_rgb_value(self.red, self.green, self.blue) * 0.01)) #value upper bound
		#self.saturationUpper=float()
		#self.valueUpper=float()


		self.hueLower=float(get_rgb_hue(self.red, self.green, self.blue) - (get_rgb_hue(self.red, self.green, self.blue) * 0.10)) #hue lower bound
		self.saturationLower=float(get_rgb_saturation(self.red, self.green, self.blue) - (get_rgb_saturation(self.red, self.green, self.blue) * 0.01)) #saturation lower bound 
		self.valueLower=float(get_rgb_value(self.red, self.green, self.blue) - (get_rgb_value(self.red, self.green, self.blue) * 0.01)) #value lower bound
		#self.saturationLower=float()
		#self.valueLower=float()

#____________________________Funcitons/Methods____________________________
def get_rgb_hue(red, green, blue):
	R = float(red/255)
	G = float(green/255)
	B = float(blue/255)
	Cmax=float(max(R,G,B))
	Cmin=float(min(R,G,B))
	delta=float(Cmax-Cmin)

	if(Cmax==R):
		return float(60*(((G-B)/delta)%6))

	if(Cmax==G):
		return float(60*(((B-R)/delta)+2))
	
	if(Cmax==B):
		return float(60*(((R-G)/delta)+4))

def get_rgb_saturation(red, green, blue):
	R = float(red/255)
	G = float(green/255)
	B = float(blue/255)
	Cmax=float(max(R,G,B))
	Cmin=float(min(R,G,B))
	delta=float(Cmax-Cmin)

	if(Cmax==0):
		return 0

	if(Cmax!=0):
		return (delta/Cmax)

def get_rgb_value(red, green, blue):
	R = float(red/255)
	G = float(green/255)
	B = float(blue/255)
	Cmax=float(max(R,G,B))
	Cmin=float(min(R,G,B))
	delta=float(Cmax-Cmin)
	
	return float(Cmax) 


def isColor(desiredColor, red, green, blue):
	inHue=get_rgb_hue(red, green, blue)
	insaturation=get_rgb_saturation(red, green, blue)
	inValue=get_rgb_value(red, green, blue)
	if desiredColor.hueUpper >= get_rgb_hue(red, green, blue) and desiredColor.hueLower <= get_rgb_hue(red, green, blue):
		if desiredColor.saturationUpper >= get_rgb_saturation(red, green, blue) and desiredColor.saturationLower <= get_rgb_saturation(red, green, blue):
			if desiredColor.saturationUpper >= get_rgb_saturation(red, green, blue) and desiredColor.saturationLower <= get_rgb_saturation(red, green, blue):
				return True
	else: 
		return False
class camera_thread(threading.Thread):#subclass of thread
	def __init__(self):
		threading.Thread.__init__(self)
		self.colorDetectionList= {}
	def getTrackingInformation(self):
		return self.colorDetectionList
	def run(self):
		#_________________________________Settings_________________________________
		#This section defines a number of global variables for use as settings
		# in the camera_thread class execution
		testing = True		#Set true if testing code should run
		debugging = True 		#Set true if Debugging code should run

		#base color RBG values for teh intended color recognition 
		defaultColors={}
		defaultColors.blue=color(0,255,0)

		green=color(0,0,255)
		orange=color(255,146,50)
		pink=color(255,91,223)


		#the webcam to capture from 
		camera = cv2.VideoCapture(0)

		#____________________________initialization____________________________
		if testing == False:
			imagecounter=1
			widthOfCircle=0
			_, initialFrame = camera.read()
			cv2.imshow('Original Picture', initialFrame)
			width = initialFrame.shape[0]
			halfW = float(width/2)
			height = initialFrame.shape[1]
			halfH = float(height/2)

			totalRedX = 0
			totalRedY = 0
			totalOrangeX=0
			totalOrangeY=0
			totalPinkX=0
			totalPinkY=0
			totalGreenX = 0
			totalGreenY = 0
			totalBlueX = 0
			totalBlueY = 0
			numberOfRedPixels = 0
			numberOfBluePixels = 0
			numberOfGreenPixels = 0
			numberOfOrangePixels=0
			numberOfPinkPixels=0
			greenExists = False
			blueExists = False
			redExists = False
			pinkExists=False
			orangeExists=False
			step = width

			for c in range(0, width):
				for r in range(0,height):
					color = initialFrame[c,r]
					#BGR
					blue = color[0]



		#_______________________________testing________________________________

		if testing==True:
			ui1 = float(raw_input("red?: "))
			ui2 = float(raw_input("green?: "))
			ui3 = float(raw_input("blue?: "))
			print  get_rgb_hue(ui1, ui2, ui3)
			print  get_rgb_saturation(ui1, ui2, ui3)
			print  get_rgb_value(ui1, ui2, ui3)


			red=color(255,0,0)
			print "Red Upper H:", red.hueUpper, " S:", red.saturationUpper, " V:", red.valueUpper
			print "Red Lower H:", red.hueLower, " S:", red.saturationLower, " V:", red.valueLower

			blue=color(0,255,0)
			print "Blue Upper H:", blue.hueUpper, " S:", blue.saturationUpper, " V:", blue.valueUpper
			print "Blue Lower H:", blue.hueLower, " S:", blue.saturationLower, " V:", blue.valueLower

			green=color(0,0,255)
			print "Green Upper H:", green.hueUpper, " S:", green.saturationUpper, " V:", green.valueUpper
			print "Green Lower H:", green.hueLower, " S:", green.saturationLower, " V:", green.valueLower

			orange=color(255,146,50)
			print "Orange Upper H:", orange.hueUpper, " S:", orange.saturationUpper, " V:", orange.valueUpper
			print "Orange Lower H:", orange.hueLower, " S:", orange.saturationLower, " V:", orange.valueLower

			pink=color(255,91,223)
			print "Pink Upper H:", pink.hueUpper, " S:", pink.saturationUpper, " V:", pink.valueUpper
			print "Pink Lower H:", pink.hueLower, " S:", pink.saturationLower, " V:", pink.valueLower

			print ("red & red"),
			print isColor(red, 255, 0, 0)

			print ("red & green"),
			print isColor(red, 0, 255, 0)

			print ("red & blue"),
			print isColor(red, 0, 0, 255)

			print ("red & orange"),
			print isColor(red, 255,146,50)

			print ("red & pink"),
			print isColor(red, 255, 91, 223)

			print ("orange & pink"),
			print isColor(orange, 255, 91, 223)