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
class color(object):
	def __init__(self, red, green, blue):



		self.red=float(red) #red
		self.green=float(green) #green
		self.blue=float(blue) #blue
		
		self.rgb=(red, green, blue)

		self.hueUpper=float(get_rgb_hue(self.red, self.green, self.blue) + (get_rgb_hue(self.red, self.green, self.blue) * 0.10)) #hue upper bound
		self.saturationUpper=float(get_rgb_saturation(self.red, self.green, self.blue) + (get_rgb_saturation(self.red, self.green, self.blue) * 0.01)) #saturation upper bound 
		self.valueUpper= float(get_rgb_value(self.red, self.green, self.blue) + (get_rgb_value(self.red, self.green, self.blue) * 0.01)) #value upper bound

		self.hueLower=float(get_rgb_hue(self.red, self.green, self.blue) - (get_rgb_hue(self.red, self.green, self.blue) * 0.10)) #hue lower bound
		self.saturationLower=float(get_rgb_saturation(self.red, self.green, self.blue) - (get_rgb_saturation(self.red, self.green, self.blue) * 0.01)) #saturation lower bound 
		self.valueLower=float(get_rgb_value(self.red, self.green, self.blue) - (get_rgb_value(self.red, self.green, self.blue) * 0.01)) #value lower bound

		totalX=0
		totalY=0
		numberOfPixels=0
		finalX=0
		finalY=0
		exists=False
		averageX=0
		averageY=0
		found=False
		width=0
		height=0



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


##############################################################################################################################################
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
		testing = False		#Set true if method/function testing code should run
		debugging = True 		#Set true if Debugging code should run

		#base color RBG values for teh intended color recognition 

		defaultColors={}
		defaultColors["blue"]=color(0,255,0)
		defaultColors["green"]=color(0,0,255)
		defaultColors["orange"]=color(255,146,50)
		defaultColors["pink"]=color(255,91,223)
		colorsCaught={}


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
			step = width

			for c in range(0, width):
				for r in range(0,height):
					color = initialFrame[c,r]
					#BGR
			        blue = color[0]
			        green = color[1]
			        red = color[2]
			        for key, item in defaultColors.iteritems()
			        	if isColor(item, red, green, blue):
			        		if debugging:
			        			initialFrame[c.r]=(item.red, item.green, item.blue)
			        		item.exists=True
			        		item.numberOfPixels+=1
			        		item.totalX+=c
			        		item.totalY+=r
			        		colorsCaught[key] = item
			        	else:
			        		if debugging:
			        			initialFrame[c,r] = (0,0,0)

			for key, item in colorsCaught.iteritems():
        		if item.numberOfPixels!=0:
        			item.finalX=item.totalX/item.numberOfPixels
        			item.finalY=item.totalY/item.numberOfPixels
        			if item.finalX>0 and item.finalX<(width-1) and item.finalY>0 and item.finalY<(height-1):
        				#determine width of the circle
        				x1=item.finalX
        				y1=item.finalY
        				x2=item.finalX
        				y2=item.finalY
        				while x1<width and isColor(item, initialFrame[x1, item.finalY][0], initialFrame[x1, item.finalY][1], initialFrame[x1, item.finalY][2]):
							if debugging:
								initialFrame[x1, item.finalY] = (255,255,255)
							x1+=1
							item.width+=1
						while x2>0 and isColor(item, initialFrame[x2, item.finalY][0], initialFrame[x2, item.finalY][1], initialFrame[x2, item.finalY][2]):
							if debugging:
								initialFrame[x2,item.finalY]=(255,255,255)
							x2-=1
							item.width+=1
						while y1<height and isColor(item, initialFrame[item.finalX,y1][0], initialFrame[item.finalY,y1][1],initialFrame[item.finalY,y1][2]):
							if debugging:
								initialFrame[item.finalX, y1] = (255,255,255)
							y1+=1
							item.height+=1
						while y2>0 and isColor(item, initialFrame[item.finalX, y2][0], initialFrame[item.finalX, y2][1], initialFrame[item.finalX, y2][2]):
							if debugging:
								initialFrame[item.finalY, y2]=(255,255,255)
							y2-=1
							item.height+=1
						if(min(item.height, item.width) < step):
							step = min(item.height, item.width)
				if item.exists:
					self.colorDetectionList[key+"X"]=item.finalX
					self.colorDetectionList[key+"Y"]=item.finalY

			emptyImg=initialFrame
			for c in range(0,width):   	#creates and empty image
				for r in range(0,height):
					emptyImg[c,r]=(0,0,0)
			########################################TRACKING LOOP#########################################
			while camera.isOpened():
				start_time=time.time()

				_,frame = camera.read()
				width = frame.shape[0]
				height = frame.shape[1]
				for item in colorsCaught.itervalues():
					item.totalY=0
					item.totalX=0
					item.numberOfPixels=0
					item.averageY=0
					item.averageX=0
					item.found=0

				if step == 0:
					step = 10
				for c in range(0, width, step/3):
					for r in range(0,height, step/3):
						color = frame[c,r]
						blue = color[0]
						green = color[1]
						red = color[2]
						for item in colorsCaught.itervalues():
							if isColor(item, red, green, blue):
								item.found=True
								currentX = c
								currentY = r
								tempX=currentX
								tempY=currentY
								rightMostX=currentX
								leftMostX=currentX
								bottomMostY=currentY
								topMostY=currentY
								while tempX<width and isColor(item, frame[tempX, currentY][0],frame[tempX, currentY][1],frame[tempX, currentY][2]):
									if debugging:
										frame[tempX,currentY]=item.rgb #is this doesnt work put them in as (item.red,item.green,item.blue)
									tempX+=1
								rightMostX=tempX
								tempX=currentX

								while tempX>1 and isColor(item, frame[tempX,currentY][0], frame[tempX,currentY][1], frame[tempX,currentY][2]):
									if debugging:
										frame[tempX, currentY]=item.rgb
									tempX-=1
								leftMostX = tempX
								while tempY<height and isColor(item, frame[currentX, tempY][0], frame[currentX, tempY][1], frame[currentX, tempY][2]):
									if debugging:
										frame[currentX,tempY]=item.rgb
									tempY+=1
								bottomMostY=tempY
								tempY=currentY
								while tempY>1 and isColor(item, frame[currentX][0], frame[currentX][1], frame[currentX][2]):
									if debugging:
										frame[currentX,tempY]=item.rgb
									tempY+=1
								topMostY=tempY

								averageX=(leftMostX+rightMostX)/2
								averageY=(bottomMostY+topMostY)/2

								


							else:
								frame[c,r]= (0,0,0) 

				

					


				






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