# -*- coding: utf-8 -*-
import numpy as np
import cv2
import scipy
from PIL import Image

camera = cv2.VideoCapture(0)
#while(True):
#for testing purposes, only take one image,
#more optimization is required to do this continuously at a reasonable rate

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
#Save original image to png
cv2.imwrite('C:\Users\Aaron\python\Original.png', frame)

for c in range(0,width):
    for r in range(0,height):
        color = frame[c,r]
        # BGR
        blue = color[0]
        green = color[1]
        red = color[2]
        if(max(blue, green, red) - min(blue, green, red))<75:
            frame[c,r] = (0,0,0)
        #blue
        elif(blue > green + 50 and blue > red + 50):
            frame[c,r] = (255,0,0)
            numberOfBluePixels = numberOfBluePixels + 1
            totalBlueX = totalBlueX + c
            totalBlueY = totalBlueY + r
        #green
        elif(green >blue + 50  and green > red + 50):
            frame[c,r] = (0,255, 0)
            numberOfBluePixels = numberOfBluePixels + 1
            totalBlueX = totalBlueX + c
            totalBlueY = totalBlueY + r
        #red
        elif(red > blue + 50 and red > green + 50):
            frame[c,r] = (0,0,255)
            numberOfRedPixels = numberOfRedPixels + 1
            totalRedX = totalRedX + c
            totalRedY = totalRedY + r
        else:
            frame[c,r] = (0,0,0)
            
            
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
        #Show center on image
        for x in range(finalBlueX-2, finalBlueX+2):
            for y in range(finalBlueY-2, finalBlueY+2):
                frame[x,y] = (255,255,255)
        for x in range(finalBlueX-1, finalBlueX+1):
            for y in range(finalBlueY-1, finalBlueY+1):
                frame[x,y] = (255,0,0)
    
if numberOfGreenPixels != 0:
# if green has been found, find average point of the color
    finalGreenX = totalGreenX/numberOfGreenPixels
    finalGreenY = totalGreenY/numberOfGreenPixels
    if finalGreenX > 0 and finalGreenX < width -1 and finalGreenY > 0 and finalGreenY < height -1:
        #Show center on image
        for x in range(finalGreenX-2, finalGreenX+2):
            for y in range(finalGreenY-2, finalGreenY+2):
                frame[x,y] = (255,255,255)
        for x in range(finalGreenX-1, finalGreenX+1):
            for y in range(finalGreenY-1, finalGreenY+1):
                frame[x,y] = (0,255,0)
            
if numberOfRedPixels != 0:
# if red has been found, find average point of the color
    finalRedX = totalRedX/numberOfRedPixels
    finalRedY = totalRedY/numberOfRedPixels
    if finalRedX > 0 and finalRedX < width -1 and finalRedY > 0 and finalRedY < height -1:
        #Show center on image
        for x in range(finalRedX-2, finalRedX+2):
            for y in range(finalRedY-2, finalRedY+2):
                frame[x,y] = (255,255,255)
        for x in range(finalRedX-1, finalRedX+1):
            for y in range(finalRedY-1, finalRedY+1):
                frame[x,y] = (0,0, 255)

#show result in a window
cv2.namedWindow('image', cv2.WINDOW_NORMAL)
cv2.imshow('image',frame)

#save result to png
cv2.imwrite('C:\Users\Aaron\python\ColorTracked.png', frame)