# -*- coding: utf-8 -*-
import cv2
import time

################ Functions ##############################
def isGrayscale(blue, green, red):
    if(max(blue, green, red) - min(blue, green, red))<25:
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
    
camera = cv2.VideoCapture(0)
imageCounter =1
################################ Initialization ##################################
widthOfCircle = 0
_, initialFrame = camera.read()
#Save original image to png
#cv2.imwrite('C:\Users\Aaron\python\Original.png', initialFrame)

width = initialFrame.shape[0]
height = initialFrame.shape[1]

totalRedX = 0
totalRedY = 0
totalGreenX = 0
totalGreenY = 0
totalBlueX = 0
totalBlueY = 0
numberOfRedPixels = 0
numberOfBluePixels = 0
numberOfGreenPixels = 0
greenExists = False
blueExists = False
redExists = False
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
    print 'Blue: ', finalBlueX, ',', finalBlueY
    print 'Green: ', finalGreenX, ',', finalGreenY
    print 'Red: ', finalRedX, ',', finalRedY
cv2.imshow('Initialization',initialFrame)          
#cv2.imwrite('C:\Users\Aaron\python\Initialized.png', initialFrame)

######################################## LOOP #####################################
#imageTitle = 'image # ' + str(imageCounter)
crap = 0
#while camera.isOpened():
crap += 1
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
numberOfRedPixels = 0
numberOfBluePixels = 0
numberOfGreenPixels = 0

averageGreenX = 0
averageGreenY = 0

averageBlueX = 0
averageBlueY = 0

averageRedX = 0
averageRedY = 0

    
blueFound= False
greenFound= False
redFound= False
print step
for c in range(0,width, step/3):
    if(((not blueExists)or(blueFound)) and ((not greenExists)or(greenFound)) and ((not redExists)or(redFound))):
        break
    for r in range(0,height, step/3):
        if(((not blueExists)or(blueFound)) and ((not greenExists)or(greenFound)) and ((not redExists)or(redFound))):
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
            frame[c,r] = (0,0,0)
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

            while tempX<width-1  and isGreen(frame[tempX,currentY][0], frame[tempX,currentY][1], frame[tempX,currentY][2]) and not isGrayscale(frame[tempX,currentY][0], frame[tempX,currentY][1], frame[tempX,currentY][2]) :
                frame[tempX, currentY] = (0,0,0)
                tempX = tempX + 1
            rightMostX = tempX
            tempX = currentX
            
            while tempX>1 and isGreen(frame[tempX,currentY][0], frame[tempX,currentY][1], frame[tempX,currentY][2]) and not isGrayscale(frame[tempX,currentY][0], frame[tempX,currentY][1], frame[tempX,currentY][2]) :
                frame[tempX, currentY] = (0,0,0)
                tempX = tempX - 1
            leftMostX = tempX
            
            while tempY<height-1 and isGreen(frame[currentX,tempY][0], frame[currentX,tempY][1], frame[currentX,tempY][2]) and not isGrayscale(frame[currentX,tempY][0], frame[tempX,currentY][1], frame[tempX,currentY][2]) :
                frame[currentX, tempY] = (0,0,0)
                tempY = tempY + 1
            BottomMostY = tempY
            tempY = currentY
            
            while tempY>1 and isGreen(frame[currentX,tempY][0], frame[currentX,tempY][1], frame[currentX,tempY][2]) and not isGrayscale(frame[currentX,tempY][0], frame[tempX,currentY][1], frame[tempX,currentY][2]):
                frame[currentX, tempY] = (0,0,0)
                tempY = tempY - 1
            topMostY = tempY
            
            averageGreenX = (leftMostX + rightMostX)/2
            averageGreenY = (bottomMostY + topMostY)/2
            
            for x in range(averageGreenX-2, averageGreenX+2):
                for y in range(averageGreenY-2, averageGreenY+2):
                    frame[x,y] = (255,255,255)
            for x in range(averageGreenX-1, averageGreenX+1):
                for y in range(averageGreenY-1, averageGreenY+1):
                    frame[x,y] = (0,255,0)
            
        #red
        elif(not redFound and isRed(blue,green,red)):
            frame[c,r] = (0,0,0)
            #find center X
            redFound = True
            redFound = True
            currentX = c
            currentY = r
            tempX = currentX
            tempY = currentY
            rightMostX = currentX
            leftMostX = currentX
            bottomMostY = currentY
            topMostY = currentY
            while tempX<width-1  and isRed(frame[tempX,currentY][0], frame[tempX,currentY][1], frame[tempX,currentY][2]) and not isGrayscale(frame[tempX,currentY][0], frame[tempX,currentY][1], frame[tempX,currentY][2]) :
                frame[tempX, currentY] = (0,0,0)
                tempX = tempX + 1
            rightMostX = tempX
            tempX = currentX
            
            while tempX>1 and isRed(frame[tempX,currentY][0], frame[tempX,currentY][1], frame[tempX,currentY][2]) and not isGrayscale(frame[tempX,currentY][0], frame[tempX,currentY][1], frame[tempX,currentY][2]):
                frame[tempX, currentY] = (0,0,0)
                tempX = tempX - 1
            leftMostX = tempX
            
            while tempY<height-1 and isRed(frame[currentX,tempY][0], frame[currentX,tempY][1], frame[currentX,tempY][2]) and not isGrayscale(frame[currentX,tempY][0], frame[tempX,currentY][1], frame[tempX,currentY][2]) :
                frame[currentX, tempY] = (0,0,0)
                tempY = tempY + 1
            BottomMostY = tempY
            tempY = currentY
            
            while tempY>1 and isRed(frame[currentX,tempY][0], frame[currentX,tempY][1], frame[currentX,tempY][2]) and not isGrayscale(frame[currentX,tempY][0], frame[tempX,currentY][1], frame[tempX,currentY][2]) :
                frame[currentX, tempY] = (0,0,0) 
                tempY = tempY - 1
            topMostY = tempY
            
            redFound = True
            
            averageRedX = (leftMostX + rightMostX)/2
            averageRedY = (bottomMostY + topMostY)/2
            
            
            for x in range(averageRedX-2, averageRedX+2):
                for y in range(averageRedY-2, averageRedY+2):
                    frame[x,y] = (255,255,255)
            for x in range(averageRedX-1, averageRedX+1):
                for y in range(averageRedY-1, averageRedY+1):
                    frame[x,y] = (0,0,255)
        #this would dramatically slow down the program
        #blue
        elif(not blueFound and isBlue(blue,green,red)):
            blueFound = True
            frame[c,r] = (0,0,0)
            currentX = c
            currentY = r
            tempX = currentX
            tempY = currentY
            rightMostX = currentX
            leftMostX = currentX
            bottomMostY = currentY
            topMostY = currentY
            while tempX < width-1 and isBlue(frame[tempX,currentY][0], frame[tempX,currentY][1], frame[tempX,currentY][2]) and not isGrayscale(frame[tempX,currentY][0], frame[tempX,currentY][1], frame[tempX,currentY][2]) :
                frame[tempX, currentX] = (0,0,0)
                print 'WTF!'
                tempX = tempX + 1
            rightMostX = tempX
            tempX = currentX
            
            while tempX>1 and isBlue(frame[tempX,currentY][0], frame[tempX,currentY][1], frame[tempX,currentY][2]) and not isGrayscale(frame[tempX,currentY][0], frame[tempX,currentY][1], frame[tempX,currentY][2]) :
                frame[tempX, currentX] = (0,0,0)    
                tempX = tempX - 1
            leftMostX = tempX
            
            while tempY<height-1 and isBlue(frame[currentX,tempY][0], frame[currentX,tempY][1], frame[currentX,tempY][2]) and not isGrayscale(frame[currentY,tempY][0], frame[tempX,currentY][1], frame[tempX,currentY][2]):
                frame[currentX, tempY] = (0,0,0)
                tempY = tempY + 1
            BottomMostY = tempY
            tempY = currentY
            
            while tempY>1 and isBlue(frame[currentX,tempY][0], frame[currentX,tempY][1], frame[currentX,tempY][2]) and not isGrayscale(frame[currentY,tempY][0], frame[tempX,currentY][1], frame[tempX,currentY][2]):
                frame[currentX, tempY] = (0,0,0)
                tempY = tempY - 1
            topMostY = tempY
            
            averageBlueX = (leftMostX + rightMostX)/2
            averageBlueY = (bottomMostY + topMostY)/2
            
            for x in range(averageBlueX-2, averageBlueX+2):
                for y in range(averageBlueY-2, averageBlueY+2):
                    frame[x,y] = (255,255,255)
            for x in range(averageBlueX-1, averageBlueX+1):
                for y in range(averageBlueY-1, averageBlueY+1):
                    frame[x,y] = (255,0,0)
            
        else:
            frame[c,r] = (0,0,0)
    
#show result in a window
if blueExists:
    print 'Blue: (', averageBlueX, ',', averageBlueY, ')' 
if greenExists:
    print 'Green: (', averageGreenX, ',', averageGreenY, ')' 
if redExists:
    print 'Red: (', averageRedX, ',', averageRedY, ')' 
imageCounter = imageCounter +1 
print("--- %s seconds ---" % (time.time() - start_time))
print "frame ", crap
cv2.imshow('imageTitle',frame)
#save result to png
##cv2.imwrite('C:\Users\Aaron\python\ColorTracked.png', frame)
#time.sleep(2)