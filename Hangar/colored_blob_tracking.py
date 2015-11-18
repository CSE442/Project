#!/usr/bin/env python2
#
# file:    colored_Blob_tracking.py
# authors: Aaron Preston, Jacob Rutowski, Lois Leport
# purpose: Provide a more organized and concise 
#	implementation of the blob color tracking from 
#	colorOptimization_2.py
# 
import cv2
import time

##########Settings


camera = cv2.VideoCapture(0)
imageCounter =1
################################ Initialization ##################################
widthOfCircle = 0
_, initialFrame = camera.read()
#Save original image to png
cv2.imwrite('C:\Users\Aaron\python\images\Original.png', initialFrame)
cv2.imshow('Original Picture', initialFrame)
width = initialFrame.shape[0]
height = initialFrame.shape[1]
#The Dictionary of colors which are applicable
colors_dict = {
	'blue'={
		#HSV color values
		'upper_bound'=(0,0,0)
		'lower_bound'=(0,0,0)
		'exists'=False
                'mat'=(255,0,0)
                'count' = 0
                'X' = 0
                'Y' = 0
                'height' = 0
                'width' = 0
	}
	'red'={
		#HSV color values
		'upper_bound'=(0,0,0)
		'lower_bound'=(0,0,0)
		'exists'=False
                'mat'=(0,0,255)
                'count' = 0
                'X' = 0
                'Y' = 0
                'height' = 0
                'width' = 0
	}
	'green'={
		#HSV color values
		'upper_bound'=(0,0,0)
		'lower_bound'=(0,0,0)
		'exists'=False
                'mat'=(0,255,0)
                'count' = 0
                'X' = 0
                'Y' = 0
                'height' = 0
                'width' = 0
	}
        'pink'={
		#HSV color values
		'upper_bound'=(0,0,0)
		'lower_bound'=(0,0,0)
		'exists'=False
                'mat' = (0,0,0)
                'count' = 0
                'X' = 0
                'Y' = 0
                'height' = 0
                'width' = 0
	}
}

#########Functions
def isColor(B,G,R,color_object):
    
    src = (B,G,R) #Array of BGR colors
    hsv = cvtColor(src, HSV, CV_BGR2HSV) #convert pixel from BGR to HSV
    return inRange((color_object['upperbound'], color_object['lowerbound'],
                    hsv))#check if in range and Return True or False

def whatColor(B,G,R):
    src = (B,G,R) #Array of BGR colors
    hsv = cvtColor(src, HSV, CV_BGR2HSV) #convert pixel from BGR to HSV
	#check if in range for each color in color_dict
        #if True, retun 'color'
    for item in color_dict:
        if inRange(item['upper_bound'], item['lower_bound'], (R,G,B}):
            item['exists']= True #Says color exists
            return item

########Variables    

for c in range(0,width):
    for r in range(0,height):
        color = initialFrame[c,r]
        blue = color[0]
        green = color[1]
        red = color[2]
        for item  in color_dict:
            if (isColor(blue, green, red, item)):
                initialframe[c,r] = item['mat']
                item['count'] += 1
                item['X'] += c
                item['Y'] += r
            else:
                initialFrame[c,r] = (0,0,0)

for item in color_dict:
    if (item['exists']):
        x1 = item['X']/item['count']
        x2 = item['X']/item['count']
        y1 = item['Y']/item['count']
        y2 = item['Y']/item['count']
        while x1<width and initialFrame[x1,item['Y']][0] == 255:
            initialFrame[x1,item['height']] = (255,255,255)
            x1 = x1+1
            item['width'] += 1
        while x2>0 and initialFrame[x2,item['Y']][0] == 255:
            initialFrame[x2,item['height']] = (255,255,255)
            x2 = x2-1
            item['width'] += 1
        while y1<height and initialFrame[item['X'],y1][0] == 255:
            initialFrame[item['width'],y1] = (255,255,255)
            y1 = y1+1
            item['height'] += 1
        while y2>0 and initialFrame[item['X'],y2][0] == 255:
            initialFrame[item['width'],y2] = (255,255,255)
            y2 = y2-1
            item['height'] += 1
        if(min(item['height'], item['width']) < step):
            step = min(item['height'], item['width'])

cv2.imshow('Initialization',initialFrame)          
######################################## LOOP #####################################

crap = 0
emptyImg = initialFrame
for c in range(0,width):
    for r in range(0,height):
        emptyImg[c,r] = (0,0,0)
for item in color_dict:
    item['X'] = 0
    item['Y'] = 0
    item['count'] = 0
    item['height'] = 0
    item['width'] = 0
    item['exists'] = False

if step == 0:
    step=10
for c in range(0,width, step/2):
    for r in range(0,height, step/3):
        color = initialFrame[c,r]
        blue = color[0]
        green = color[1]
        red = color[2]
        for item in color_dict:
            if (isColor(blue, green, red, item) and not item['exists']):
                item['exists'] = True
                item['X'],tempX,topX,botX = c
                item['Y'],tempY,topY,botY = r

                while (tempX<width  and isColor(blue, green, red, item)):
                    frame[tempX, item['Y']] = (0,255,0)
                    tempX = tempX + 1
                botX = tempX
                tempX = item['X']

                while (tempX>1 and isColor(blue, green, red, item)):
                    frame[tempX, item['Y']] = (0,255,0)
                    tempX = tempX - 1
                topX = tempX

                 while (tempY<height and isColor(blue, green, red, item)):
                    frame[currentX, tempY] = (0,255,0)
                    tempY = tempY + 1
                botMostY = tempY
                tempY = currentY
                
                while (tempY>1 and isColor(blue, green, red, item)):
                    frame[item['X'], tempY] = (0,255,0) 
                    tempY = tempY - 1
                topY = tempY
                
                item['X'] = (topX + botX)/2
                item['Y'] = (botY + topY)/2
                
                for x in range(item['X']-2, item['X']+2):
                    for y in range(item['Y']-2, item['Y']+2):
                        if y>0 and y<height and x>0 and x<width:
                            frame[x,y] = (255,255,255)
                for x in range(item['X']-1, item['X']+1):
                    for y in range(item['Y']-1, item['Y']+1):
                        if y>0 and y<height and x>0 and x<width:
                            frame[x,y] = item['mat']
