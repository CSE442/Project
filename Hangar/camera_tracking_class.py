#!/usr/bin/env python2
#
# file:    camera_tracking_class.py
# authors: Jacob Rutowski
# purpose: provide a class definition of the camera tracking object to better suit the main.py implementation
#
import cv2
import time
import math
import thread
import threading
import channel


################ Functions ##############################
def isGrayscale(blue, green, red):
    if(max(blue, green, red) - min(blue, green, red))<70:
        return True
    else:
        return False

def isBlue(blue, green, red):
    if(blue > green and blue > red ):
        return True
    else:
        return False

def isGreen(blue, green, red):
    if green > blue and green > red:
        return True
    else:
        return False

def isRed(blue, green, red):
    if red > blue and red > green:
        return True
    else:
        return False

def isOrange(blue, green, red):
    #if ( red>=((green/2)*0.9 ) and ( red<=((green/2)*1.1 )
    if ((red-(2*green))/red <= 0.1) and ((red-(4*blue))/red <= 0.1) and ((green-(2*blue))/green <= 0.1):
        return True
    else:
        return False

def isPink(blue, green, red):
    if (   (red-(2*blue))/red <= 0.1) and ((red-(4*green))/red <= 0.1) and ((blue-(2*green))/blue <= 0.1):
        return True
    else:
        return False

class carPlacement(object):
	def __init__(self,front, back, angle):
		self.front = front
		self.back = back
		self.angle = angle

		self.avgX = ((front[0]+back[0])/2)
		self.avgY = ((front[1]+back[1])/2)
		self.position = (avgX,avgY)




class camera_thread(threading.Thread):#subclass of thread
	def __init__(self):
		threading.Thread.__init__(self)
		self.colorDetectionList= {}
		self.placementData = ((0.0,0.0),(0.0,0.0),0.0)

	def getTrackingInformation(self):
		return self.placementData

        def kill(self):
            thread.exit()

	def run(self):
		camera = cv2.VideoCapture(0)
		imageCounter =1
		################################ Initialization ##################################

		widthOfCircle = 0
		_, initialFrame = camera.read()
		#Save original image to png
		#cv2.imwrite('C:\Users\Aaron\python\images\Original.png', initialFrame)
		#cv2.imshow('Original Picture', initialFrame)
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

		for c in range(0,width):
		    for r in range(0,height):
		        color = initialFrame[c,r]
		        # BGR
		        blue = color[0]
		        green = color[1]
		        red = color[2]
		        if(isGrayscale(blue, green, red)):
		            initialFrame[c,r] = (0,0,0)
		        #green
		        elif(isGreen(blue, green, red)):
		            initialFrame[c,r] = (0,255, 0)
		            greenExists = True
		            numberOfGreenPixels = numberOfGreenPixels + 1
		            totalGreenX = totalGreenX + c
		            totalGreenY = totalGreenY + r
		        #blue
		        elif(isBlue(blue, green, red)):
		            initialFrame[c,r] = (255,0,0)
		            blueExists = True
		            numberOfBluePixels = numberOfBluePixels + 1
		            totalBlueX = totalBlueX + c
		            totalBlueY = totalBlueY + r

		        # #pink
		        # elif(isPink(blue, green, red)):
		        #     initialFrame[c,r] = (64,127,255)
		        #     pinkExists = True
		        #     numberOfPinkPixels = numberOfPinkPixels + 1
		        #     totalPinkX = totalPinkX + c
		        #     totalPinkY = totalPinkY + r

		        # #orange
		        # elif(isOrange(blue, green, red)):
		        #     initialFrame[c,r] = (127,64,255)
		        #     orangeExists = True
		        #     numberOfOrangePixels = numberOfOrangePixels + 1
		        #     totalOrangeX = totalOrangeX + c
		        #     totalOrangeY = totalOrangeY + r

		        #red
		        elif(isRed(blue, green, red)):
		            initialFrame[c,r] = (0,0,255)
		            redExists = True
		            numberOfRedPixels = numberOfRedPixels + 1
		            totalRedX = totalRedX + c
		            totalRedY = totalRedY + r
		        else:
		            initialFrame[c,r] = (0,0,0)

		finalBlueX = 0
		finalBlueY = 0
		finalGreenX = 0
		finalGreenY = 0
		finalRedX = 0
		finalRedY = 0
		finalPinkX=0
		finalPinkY=0
		finalorangeX=0
		finalOrangeY=0

		if numberOfBluePixels != 0:
		# if blue has been found, find average point of the color
		    finalBlueX = totalBlueX/numberOfBluePixels
		    finalBlueY = totalBlueY/numberOfBluePixels
		    if finalBlueX > 0 and finalBlueX < width -1 and finalBlueY > 0 and finalBlueY < height -1:
		        #determine width of the circle
		        blueWidth = 0
		        blueHeight = 0
		        x1 = finalBlueX
		        y1 = finalBlueY
		        x2 = finalBlueX
		        y2 = finalBlueY
		        while x1<width and initialFrame[x1,finalBlueY][0] == 255:
		            initialFrame[x1,finalBlueY] = (255,255,255)
		            x1 = x1+1
		            blueWidth = blueWidth + 1
		        while x2>0 and initialFrame[x2,finalBlueY][0] == 255:
		            initialFrame[x2,finalBlueY] = (255,255,255)
		            x2 = x2-1
		            blueWidth = blueWidth + 1
		        while y1<height and initialFrame[finalBlueX,y1][0] == 255:
		            initialFrame[finalBlueX,y1] = (255,255,255)
		            y1 = y1+1
		            blueHeight = blueHeight + 1
		        while y2>0 and initialFrame[finalBlueX,y2][0] == 255:
		            initialFrame[finalBlueX,y2] = (255,255,255)
		            y2 = y2-1
		            blueHeight = blueHeight + 1
		        if(min(blueHeight, blueWidth) < step):
		            step = min(blueHeight, blueWidth)


		if numberOfGreenPixels != 0:
		# if green has been found, find average point of the color
		    finalGreenX = totalGreenX/numberOfGreenPixels
		    finalGreenY = totalGreenY/numberOfGreenPixels
		    if finalGreenX > 0 and finalGreenX < width -1 and finalGreenY > 0 and finalGreenY < height -1:
		        #Show center on image
		        for x in range(finalGreenX-2, finalGreenX+2):
		            for y in range(finalGreenY-2, finalGreenY+2):
		                initialFrame[x,y] = (255,255,255)
		        for x in range(finalGreenX-1, finalGreenX+1):
		            for y in range(finalGreenY-1, finalGreenY+1):
		                initialFrame[x,y] = (0,255,0)
		        greenWidth = 0
		        greenHeight = 0
		        x1 = finalGreenX
		        y1 = finalGreenY
		        x2 = finalGreenX
		        y2 = finalGreenY
		        while x1<width and initialFrame[x1,finalGreenY][1] == 255:
		            initialFrame[x1,finalGreenY] = (255,255,255)
		            x1 = x1+1
		            greenWidth = greenWidth + 1
		        while x2>0 and initialFrame[x2,finalGreenY][1] == 255:
		            initialFrame[x2,finalGreenY] = (255,255,255)
		            x2 = x2-1
		            greenWidth = greenWidth + 1
		        while y1<height and initialFrame[finalGreenX,y1][1] == 255:
		            initialFrame[finalGreenX,y1] = (255,255,255)
		            y1 = y1+1
		            greenHeight = greenHeight + 1
		        while y2>0 and initialFrame[finalGreenX,y2][1] == 255:
		            initialFrame[finalGreenX,y2] = (255,255,255)
		            y2 = y2-1
		            greenHeight = greenHeight + 1

		        if(min(greenHeight, greenWidth) < step):
		            step = min(greenHeight, greenWidth)

		# if numberOfPinkPixels != 0:
		# # if Pink has been found, find average point of the color
		#     finalPinkX = totalPinkX/numberOfPinkPixels
		#     finalPinkY = totalPinkY/numberOfPinkPixels
		#     if finalPinkX > 0 and finalPinkX < width -1 and finalPinkY > 0 and finalPinkY < height -1:
		#         pinkWidth = 0
		#         pinkHeight = 0
		#         x1 = finalPinkX
		#         y1 = finalPinkY
		#         x2 = finalPinkX
		#         y2 = finalPinkY
		#         while x1<width and isPink(initialFrame[x1,finalPinkY][0],initialFrame[x1,finalPinkY][1],initialFrame[x1,finalPinkY][2]):
		#             initialFrame[x1,finalPinkY] = (255,255,255)
		#             x1 = x1+1
		#             pinkWidth = pinkWidth + 1
		#         while x2>0 and isPink(initialFrame[x2,finalPinkY][0],initialFrame[x2,finalPinkY][1],initialFrame[x2,finalPinkY][2]):
		#             initialFrame[x2,finalPinkY] = (255,255,255)
		#             x2 = x2-1
		#             pinkWidth = pinkWidth + 1
		#         while y1<height and isPink(initialFrame[finalPinkX,y1][0],initialFrame[finalPinkX,y1][1],initialFrame[finalPinkX,y1][2]):
		#             initialFrame[finalPinkX,y1] = (255,255,255)
		#             y1 = y1+1
		#             pinkHeight = pinkHeight + 1
		#         while y2>0 and isPink(initialFrame[finalPinkX,y2][0],initialFrame[finalPinkX,y2][1],initialFrame[finalPinkX,y2][2]):
		#             initialFrame[finalPinkX,y2] = (255,255,255)
		#             y2 = y2-1
		#             pinkHeight = pinkHeight + 1
		#         if(min(pinkHeight, pinkWidth) < step):
		#             step = min(pinkHeight, pinkWidth)

		# if numberOfOrangePixels != 0:
		# # if Pink has been found, find average point of the color
		#     finalOrangeX = totalOrangeX/numberOfOrangePixels
		#     finalOrangeY = totalOrangeY/numberOfOrangePixels
		#     if finalOrangeX > 0 and finalOrangeX < width -1 and finalOrangeY > 0 and finalOrangeY < height -1:
		#         OrangeWidth = 0
		#         OrangeHeight = 0
		#         x1 = finalOrangeX
		#         y1 = finalOrangeY
		#         x2 = finalOrangeX
		#         y2 = finalOrangeY
		#         while x1<width and isOrange(initialFrame[x1,finalOrangeY][0],initialFrame[x1,finalOrangeY][1],initialFrame[x1,finalOrangeY][2]):
		#             initialFrame[x1,finalOrangeY] = (255,255,255)
		#             x1 = x1+1
		#             OrangeWidth = OrangeWidth + 1
		#         while x2>0 and isOrange(initialFrame[x2,finalOrangeY][0],initialFrame[x2,finalOrangeY][1],initialFrame[x2,finalOrangeY][2]):
		#             initialFrame[x2,finalOrangeY] = (255,255,255)
		#             x2 = x2-1
		#             OrangeWidth = OrangeWidth + 1
		#         while y1<height and isOrange(initialFrame[finalOrangeY,y1][0],initialFrame[finalOrangeY,y1][1],initialFrame[finalOrangeY,y1][2]):
		#             initialFrame[finalOrangeX,y1] = (255,255,255)
		#             y1 = y1+1
		#             OrangeHeight = OrangeHeight + 1
		#         while y2>0 and isOrange(initialFrame[finalOrangeY,y2][0],initialFrame[finalOrangeY,y2][1],initialFrame[finalOrangeY,y2][2]):
		#             initialFrame[finalOrangeX,y2] = (255,255,255)
		#             y2 = y2-1
		#             OrangeHeight = OrangeHeight + 1
		#         if(min(OrangeHeight, OrangeWidth) < step):
		#             step = min(OrangeHeight, OrangeWidth)

		if numberOfRedPixels != 0:
		# if red has been found, find average point of the color
		    finalRedX = totalRedX/numberOfRedPixels
		    finalRedY = totalRedY/numberOfRedPixels
		    if finalRedX > 0 and finalRedX < width -1 and finalRedY > 0 and finalRedY < height -1:
		        redWidth = 0
		        redHeight = 0
		        x1 = finalRedX
		        y1 = finalRedY
		        x2 = finalRedX
		        y2 = finalRedY
		        while x1<width and initialFrame[x1,finalRedY][2] == 255:
		            initialFrame[x1,finalRedY] = (255,255,255)
		            x1 = x1+1
		            redWidth = redWidth + 1
		        while x2>0 and initialFrame[x2,finalRedY][2] == 255:
		            initialFrame[x2,finalRedY] = (255,255,255)
		            x2 = x2-1
		            redWidth = redWidth + 1
		        while y1<height and initialFrame[finalRedX,y1][2] == 255:
		            initialFrame[finalRedX,y1] = (255,255,255)
		            y1 = y1+1
		            redHeight = redHeight + 1
		        while y2>0 and initialFrame[finalRedX,y2][2] == 255:
		            initialFrame[finalRedX,y2] = (255,255,255)
		            y2 = y2-1
		            redHeight = redHeight + 1
		        if(min(redHeight, redWidth) < step):
		            step = min(redHeight, redWidth)
		    #For debugging purposes, compares non optimized centers to optimized, in-loop centers
		    #print 'Blue: ', finalBlueX, ',', finalBlueY
		    #print 'Green: ', finalGreenX, ',', finalGreenY
		    #print 'Red: ', finalRedX, ',', finalRedY
		#cv2.imshow('Initialization',initialFrame)
		#cv2.imwrite('C:\Users\Aaron\python\images\Initialized.png', initialFrame)

		#Generates the dectected color blob values to pass along
		#colorDetectionList= {}
		if blueExists:
		    self.colorDetectionList['blueX']=finalBlueX
		    self.colorDetectionList['blueY']=finalBlueY

		if greenExists:
		    self.colorDetectionList['greenX']=finalGreenX
		    self.colorDetectionList['greenY']=finalGreenY

		if redExists:
		    self.colorDetectionList['redX']=finalRedX
		    self.colorDetectionList['redY']=finalRedY

		if greenExists and redExists:
		    deltaY=finalGreenY-finalRedY
		    deltaX=finalGreenX-finalRedX
		    angleInDegrees = math.atan2(deltaX, deltaY) * 180 / math.pi
		    self.colorDetectionList['Red To Green']=angleInDegrees





		######################################## LOOP #####################################
		#imageTitle = 'image # ' + str(imageCounter)
		crap = 0
		emptyImg = initialFrame
		for c in range(0,width):
		    for r in range(0,height):
		        emptyImg[c,r] = (0,0,0)

		while camera.isOpened():
		    start_time = time.time()
		    ##for testing purposes, only take one image,
		    ##more optimization is required to do this continuously at a reasonable rate (than one img every 3 seconds)

		    #Reads a frame from the camera and stores
		    _, frame = camera.read()

		    width = frame.shape[0]
		    height = frame.shape[1]

		    totalRedX = 0
		    totalRedY = 0
		    totalGreenX = 0
		    totalGreenY = 0
		    totalBlueX = 0
		    totalBlueY = 0
		    totalOrangeY=0
		    totalOrangeX=0
		    totalPinkY=0
		    totalPinkX=0
		    numberOfRedPixels = 0
		    numberOfBluePixels = 0
		    numberOfGreenPixels = 0
		    numberOfOrangePixels=0
		    numberOfPinkPixels=0

		    averageGreenX = 0
		    averageGreenY = 0

		    averageBlueX = 0
		    averageBlueY = 0

		    averageRedX = 0
		    averageRedY = 0

		    averagePinkX=0
		    averagePinkY=0

		    averageOrangeX=0
		    averageOrangeY=0

		    blueFound= False
		    greenFound= False
		    redFound= False
		    orangeFound=False
		    pinkFound=False

		    if step == 0:
		        step = 10
		    for c in range(0,width, step/2):
		        if(((not blueExists)or(blueFound)) and ((not greenExists)or(greenFound)) and ((not redExists)or(redFound)) and ((not orangeExists)or(orangeFound))and((not pinkExists)or(pinkFound))):
		            break
		        for r in range(0,height, step/3):
		            if(((not blueExists)or(blueFound)) and ((not greenExists)or(greenFound)) and ((not redExists)or(redFound)) and ((not orangeExists)or(orangeFound))and((not pinkExists)or(pinkFound))):
		                break
		            color = frame[c,r]
		            # BGR
		            blue = color[0]
		            green = color[1]
		            red = color[2]
		            if isGrayscale(blue, green, red):
		                frame[c,r] = (0,0,0)
		            #green
		            elif(not greenFound and isGreen(blue,green,red)):
		                #find center X
		                greenFound = True
		                currentX = c
		                currentY = r
		                tempX = currentX
		                tempY = currentY
		                rightMostX = currentX
		                leftMostX = currentX
		                bottomMostY = currentY
		                topMostY = currentY

		                while tempX<width  and isGreen(frame[tempX,currentY][0], frame[tempX,currentY][1], frame[tempX,currentY][2]) and not isGrayscale(frame[tempX,currentY][0], frame[tempX,currentY][1], frame[tempX,currentY][2]) :
		                    frame[tempX, currentY] = (0,255,0)
		                    tempX = tempX + 1
		                rightMostX = tempX
		                tempX = currentX

		                while tempX>1 and isGreen(frame[tempX,currentY][0], frame[tempX,currentY][1], frame[tempX,currentY][2]) and not isGrayscale(frame[tempX,currentY][0], frame[tempX,currentY][1], frame[tempX,currentY][2]):
		                    frame[tempX, currentY] = (0,255,0)
		                    tempX = tempX - 1
		                leftMostX = tempX

		                while tempY<height and isGreen(frame[currentX,tempY][0], frame[currentX,tempY][1], frame[currentX,tempY][2]) and not isGrayscale(frame[currentX,tempY][0], frame[currentX,tempY][1], frame[currentX,tempY][2]) :
		                    frame[currentX, tempY] = (0,255,0)
		                    tempY = tempY + 1
		                bottomMostY = tempY
		                tempY = currentY

		                while tempY>1 and isGreen(frame[currentX,tempY][0], frame[currentX,tempY][1], frame[currentX,tempY][2]) and not isGrayscale(frame[currentX,tempY][0], frame[currentX,tempY][1], frame[currentX,tempY][2]) :
		                    frame[currentX, tempY] = (0,255,0)
		                    tempY = tempY - 1
		                topMostY = tempY

		                averageGreenX = (leftMostX + rightMostX)/2
		                averageGreenY = (bottomMostY + topMostY)/2

		                for x in range(averageGreenX-2, averageGreenX+2):
		                    for y in range(averageGreenY-2, averageGreenY+2):
		                        if y>0 and y<height and x>0 and x<width:
		                            frame[x,y] = (255,255,255)
		                for x in range(averageGreenX-1, averageGreenX+1):
		                    for y in range(averageGreenY-1, averageGreenY+1):
		                        if y>0 and y<height and x>0 and x<width:
		                            frame[x,y] = (0,255,0)
		            #blue
		            elif(not blueFound and isBlue(blue,green,red)):
		                blueFound = True
		                currentX = c
		                currentY = r
		                tempX = currentX
		                tempY = currentY
		                rightMostX = currentX
		                leftMostX = currentX
		                bottomMostY = currentY
		                topMostY = currentY
		                while tempX < width and isBlue(frame[tempX,currentY][0], frame[tempX,currentY][1], frame[tempX,currentY][2]) and not isGrayscale(frame[tempX,currentY][0], frame[tempX,currentY][1], frame[tempX,currentY][2]) :
		                    frame[tempX, currentY] = (255,0,0)
		                    tempX = tempX + 1
		                rightMostX = tempX
		                tempX = currentX

		                while tempX>1 and isBlue(frame[tempX,currentY][0], frame[tempX,currentY][1], frame[tempX,currentY][2]) and not isGrayscale(frame[tempX,currentY][0], frame[tempX,currentY][1], frame[tempX,currentY][2]) :
		                    frame[tempX, currentY] = (255,0,0)
		                    tempX = tempX - 1
		                leftMostX = tempX

		                while tempY<height and isBlue(frame[currentX,tempY][0], frame[currentX,tempY][1], frame[currentX,tempY][2]) and not isGrayscale(frame[currentX,tempY][0], frame[currentX,tempY][1], frame[currentX,tempY][2]):
		                    frame[currentX, tempY] = (255,0,0)
		                    tempY = tempY + 1
		                bottomMostY = tempY
		                tempY = currentY

		                while tempY>1 and isBlue(frame[currentX,tempY][0], frame[currentX,tempY][1], frame[currentX,tempY][2]) and not isGrayscale(frame[currentX,tempY][0], frame[currentX,tempY][1], frame[currentX,tempY][2]):
		                    frame[currentX, tempY] = (255,0,0)
		                    tempY = tempY - 1
		                topMostY = tempY

		                averageBlueX = (leftMostX + rightMostX)/2
		                averageBlueY = (bottomMostY + topMostY)/2

		                for x in range(averageBlueX-2, averageBlueX+2):
		                    for y in range(averageBlueY-2, averageBlueY+2):
		                        if y>0 and y<height and x>0 and x<width:
		                            frame[x,y] = (255,255,255)
		                for x in range(averageBlueX-1, averageBlueX+1):
		                    for y in range(averageBlueY-1, averageBlueY+1):
		                        if y>0 and y<height and x>0 and x<width:
		                            frame[x,y] = (255,0,0)

		            # #pink
		            # elif(not pinkFound and isPink(blue,green,red)):
		            #     #find center X
		            #     pinkFound = True
		            #     currentX = c
		            #     currentY = r
		            #     tempX = currentX
		            #     tempY = currentY
		            #     rightMostX = currentX
		            #     leftMostX = currentX
		            #     bottomMostY = currentY
		            #     topMostY = currentY

		            #     while tempX<width  and isPink(frame[tempX,currentY][0], frame[tempX,currentY][1], frame[tempX,currentY][2]) and not isGrayscale(frame[tempX,currentY][0], frame[tempX,currentY][1], frame[tempX,currentY][2]) :
		            #         frame[tempX, currentY] = (64,127,255)
		            #         tempX = tempX + 1
		            #     rightMostX = tempX
		            #     tempX = currentX

		            #     while tempX>1 and isPink(frame[tempX,currentY][0], frame[tempX,currentY][1], frame[tempX,currentY][2]) and not isGrayscale(frame[tempX,currentY][0], frame[tempX,currentY][1], frame[tempX,currentY][2]):
		            #         frame[tempX, currentY] = (64,127,255)
		            #         tempX = tempX - 1
		            #     leftMostX = tempX

		            #     while tempY<height and isPink(frame[currentX,tempY][0], frame[currentX,tempY][1], frame[currentX,tempY][2]) and not isGrayscale(frame[currentX,tempY][0], frame[tempX,currentY][1], frame[tempX,currentY][2]) :
		            #         frame[currentX, tempY] = (64,127,255)
		            #         tempY = tempY + 1
		            #     bottomMostY = tempY
		            #     tempY = currentY

		            #     while tempY>1 and isPink(frame[currentX,tempY][0], frame[currentX,tempY][1], frame[currentX,tempY][2]) and not isGrayscale(frame[currentX,tempY][0], frame[tempX,currentY][1], frame[tempX,currentY][2]) :
		            #         frame[currentX, tempY] = (64,127,255)
		            #         tempY = tempY - 1
		            #     topMostY = tempY

		            #     pinkFound = True

		            #     averagePinkX = (leftMostX + rightMostX)/2
		            #     averagePinkY = (bottomMostY + topMostY)/2


		            #     for x in range(averagePinkX-2, averagePinkX+2):
		            #         for y in range(averagePinkY-2, averagePinkY+2):
		            #             if y>0 and y<height and x>0 and x<width:
		            #                 frame[x,y] = (255,255,255)
		            #     for x in range(averagePinkX-1, averagePinkX+1):
		            #         for y in range(averagePinkY-1, averagePinkY+1):
		            #             if y>0 and y<height and x>0 and x<width:
		            #                 frame[x,y] = (64,127,255)


		            # #orange
		            # elif(not orangeFound and isOrange(blue,green,red)):
		            #     #find center X
		            #     orangeFound = True
		            #     currentX = c
		            #     currentY = r
		            #     tempX = currentX
		            #     tempY = currentY
		            #     rightMostX = currentX
		            #     leftMostX = currentX
		            #     bottomMostY = currentY
		            #     topMostY = currentY

		            #     while tempX<width  and isOrange(frame[tempX,currentY][0], frame[tempX,currentY][1], frame[tempX,currentY][2]) and not isGrayscale(frame[tempX,currentY][0], frame[tempX,currentY][1], frame[tempX,currentY][2]) :
		            #         frame[tempX, currentY] = (127,64,255)
		            #         tempX = tempX + 1
		            #     rightMostX = tempX
		            #     tempX = currentX

		            #     while tempX>1 and isOrange(frame[tempX,currentY][0], frame[tempX,currentY][1], frame[tempX,currentY][2]) and not isGrayscale(frame[tempX,currentY][0], frame[tempX,currentY][1], frame[tempX,currentY][2]):
		            #         frame[tempX, currentY] = (127,64,255)
		            #         tempX = tempX - 1
		            #     leftMostX = tempX

		            #     while tempY<height and isOrange(frame[currentX,tempY][0], frame[currentX,tempY][1], frame[currentX,tempY][2]) and not isGrayscale(frame[currentX,tempY][0], frame[tempX,currentY][1], frame[tempX,currentY][2]) :
		            #         frame[currentX, tempY] = (127,64,255)
		            #         tempY = tempY + 1
		            #     bottomMostY = tempY
		            #     tempY = currentY

		            #     while tempY>1 and isOrange(frame[currentX,tempY][0], frame[currentX,tempY][1], frame[currentX,tempY][2]) and not isGrayscale(frame[currentX,tempY][0], frame[tempX,currentY][1], frame[tempX,currentY][2]) :
		            #         frame[currentX, tempY] = (127,64,255)
		            #         tempY = tempY - 1
		            #     topMostY = tempY

		            #     orangeFound = True

		            #     averageOrangeX = (leftMostX + rightMostX)/2
		            #     averageOrangeY = (bottomMostY + topMostY)/2


		            #     for x in range(averageOrangeX-2, averageOrangeX+2):
		            #         for y in range(averageOrangeY-2, averageOrangeY+2):
		            #             if y>0 and y<height and x>0 and x<width:
		            #                 frame[x,y] = (255,255,255)
		            #     for x in range(averageOrangeX-1, averageOrangeX+1):
		            #         for y in range(averageOrangeY-1, averageOrangeY+1):
		            #             if y>0 and y<height and x>0 and x<width:
		            #                 frame[x,y] = (127,64,255)

		            #red
		            elif(not redFound and isRed(blue,green,red)):
		                #find center X
		                redFound = True
		                currentX = c
		                currentY = r
		                tempX = currentX
		                tempY = currentY
		                rightMostX = currentX
		                leftMostX = currentX
		                bottomMostY = currentY
		                topMostY = currentY
		                #print '(X,Y): ', currentX, currentY
		                #print 'X < Width:', tempX<width
		                #print 'Pixel is red: ',isRed(frame[tempX,currentY][0], frame[tempX,currentY][1], frame[tempX,currentY][2])
		                #print 'is grayscale?: ', isGrayscale(frame[tempX,currentY][0], frame[tempX,currentY][1], frame[tempX,currentY][2])

		                while tempX<width  and isRed(frame[tempX,currentY][0], frame[tempX,currentY][1], frame[tempX,currentY][2]) and not isGrayscale(frame[tempX,currentY][0], frame[tempX,currentY][1], frame[tempX,currentY][2]) :
		                    frame[tempX, currentY] = (0,0,255)
		                    tempX = tempX + 1
		                rightMostX = tempX
		                tempX = currentX

		                while tempX>1 and isRed(frame[tempX,currentY][0], frame[tempX,currentY][1], frame[tempX,currentY][2]) and not isGrayscale(frame[tempX,currentY][0], frame[tempX,currentY][1], frame[tempX,currentY][2]):
		                    frame[tempX, currentY] = (0,0,255)
		                    tempX = tempX - 1
		                leftMostX = tempX

		                while tempY<height and isRed(frame[currentX,tempY][0], frame[currentX,tempY][1], frame[currentX,tempY][2]) and not isGrayscale(frame[currentX,tempY][0], frame[tempX,currentY][1], frame[tempX,currentY][2]) :
		                    frame[currentX, tempY] = (0,0,255)
		                    tempY = tempY + 1
		                bottomMostY = tempY
		                tempY = currentY

		                while tempY>1 and isRed(frame[currentX,tempY][0], frame[currentX,tempY][1], frame[currentX,tempY][2]) and not isGrayscale(frame[currentX,tempY][0], frame[tempX,currentY][1], frame[tempX,currentY][2]) :
		                    frame[currentX, tempY] = (0,0,255)
		                    tempY = tempY - 1
		                topMostY = tempY

		                redFound = True

		                averageRedX = (leftMostX + rightMostX)/2
		                averageRedY = (bottomMostY + topMostY)/2


		                for x in range(averageRedX-2, averageRedX+2):
		                    for y in range(averageRedY-2, averageRedY+2):
		                        if y>0 and y<height and x>0 and x<width:
		                            frame[x,y] = (255,255,255)
		                for x in range(averageRedX-1, averageRedX+1):
		                    for y in range(averageRedY-1, averageRedY+1):
		                        if y>0 and y<height and x>0 and x<width:
		                            frame[x,y] = (0,0,255)

		            #else:
		            #    frame[c,r] = (0,0,0)
		            #this interferes with finding centers


		    #For debugging purposes, compares non optimized centers to optimized, in-loop centers

		    #TODO Fix X and Y
		    #X and Y are swapped for some reason that I can't figure out
		    #an actual fix so I just switched them at the end.
		    #-Louis

		    if blueFound:
		        coordinateBlueY = float(averageBlueY-(halfH))/(halfH)
		        coordinateBlueX = float(-(averageBlueX-(halfW))/(halfW))
		        #print 'Blue: (', coordinateBlueY, ',', coordinateBlueX, ')'
		        self.colorDetectionList['blueX']=coordinateBlueY
		        self.colorDetectionList['blueY']=coordinateBlueX
		    if greenFound:
		        coordinateGreenY = float(averageGreenY-(halfH))/(halfH)
		        coordinateGreenX = float(-(averageGreenX-(halfW))/(halfW))
		        #print 'Green: (', coordinateGreenY, ',', coordinateGreenX, ')'
		        self.colorDetectionList['greenX']=coordinateGreenY
		        self.colorDetectionList['greenY']=coordinateGreenX
		    # if pinkFound:
		    #     print 'Pink: (', averagePinkX, ',', averagePinkY, ')'
		    # if orangeFound:
		    #     print 'Orange: (', averageOrangeX, ',', averageOrangeY, ')'
		    if redFound:
		        coordinateRedY = float(averageRedY-(halfH))/(halfH)
		        coordinateRedX = float(-(averageRedX-(halfW))/(halfW))
		        #print 'Red: (', coordinateRedY, ',', coordinateRedX, ')'
		        self.colorDetectionList['redX']=coordinateRedY
		        self.colorDetectionList['redY']=coordinateRedX

		    if greenFound and redFound:
		        deltaY=averageGreenY-averageRedY
		        deltaX=averageGreenX-averageRedX
		        if (True):
		            angleInDegrees = math.atan2(deltaY,deltaX) +math.pi/2
		        self.colorDetectionList['Red To Green']=angleInDegrees

		    outputImg = emptyImg
		    if blueExists:
		        for x in range(averageBlueX-2, averageBlueX+2):
		            for y in range(averageBlueY-2, averageBlueY+2):
		                if x>0 and x<width and y>0 and y < height:
		                    outputImg[x, y] = (255,0,0)
		    if greenExists:
		        for x in range(averageGreenX-2, averageGreenX+2):
		            for y in range(averageGreenY-2, averageGreenY+2):
		                if x>0 and x<width and y>0 and y < height:
		                    outputImg[x, y] = (0,255,0)
		    # if pinkExists:
		    #     for x in range(averagePinkX-2, averagePinkX+2):
		    #         for y in range(averagePinkY-2, averagePinkY+2):
		    #             if x>0 and x<width and y>0 and y < height:
		    #                 outputImg[x, y] = (127,64,255)
		    # if orangeExists:
		    #     for x in range(averageOrangeX-2, averageOrangeX+2):
		    #         for y in range(averageOrangeY-2, averageOrangeY+2):
		    #             if x>0 and x<width and y>0 and y < height:
		    #                 outputImg[x, y] = (64,127,255)
		    if redExists:
		        for x in range(averageRedX-2, averageRedX+2):
		            for y in range(averageRedY-2, averageRedY+2):
		                if x>0 and x<width and y>0 and y < height:
		                    outputImg[x, y] = (0,0,255)
		    imageCounter = imageCounter +1
		    self.placementData = ((coordinateGreenY,coordinateGreenX),(coordinateRedY,coordinateRedX),angleInDegrees)



		    # if start_time != time.time():
		    #     self.colorDetectionList['---fps---']= 1/(time.time() - start_time)

		    #send_channel.send(self.colorDetectionList)

		   #  print("Dictionary: ")
		   #  for item in self.colorDetectionList:
		   #      print item, ': ', self.colorDetectionList[item]

		   #  print("--- %s fps ---" % (1/(time.time() - start_time)))
		   #  print "frame ", crap
		   # #cv2.imshow('imageTitle',outputImg)
		    #save result to png
		    #cv2.imwrite('C:\Users\Aaron\python\images\ColorTracked.png', frame)
		    #cv2.imshow('Initialization',frame)
		    #time.sleep(2)
		    k = cv2.waitKey(5) & 0xFF
		    if k == 27:
		        thread.exit()
		        break

